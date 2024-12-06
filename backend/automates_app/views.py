from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.http import JsonResponse, HttpResponseRedirect
import random
import string
import requests
from django.conf import settings
from .models import Draft, UserToken


@login_required
def home(request):
    return render(request, "home.html", {})

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("automates_app:login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def delete_account(request):
    if request.method == "POST":
        # Get the current user
        user = request.user

        # Log the user out first
        logout(request)

        # Delete the user from the database
        user.delete()

        # Redirect to home after deletion
        return redirect("automates_app:home")
    else:
        return HttpResponseForbidden("Invalid request method")

def accounts(request):
    return render(request, "accounts.html")

def generate_description_view(request):
    description = ""
    if request.method == 'POST':
        repo_link = request.POST.get('repositoryLink')
        user_description = request.POST.get('userDescription', "")
        audience = request.POST.get('audience')
        tone = request.POST.get('tone')
        style = request.POST.get('style')
        hashtags = request.POST.get('hashtags')
        draft = Draft(
            repositoryLink=repo_link,
            userDescription=user_description,
            postAudience=audience,
            postTone=tone,
            postStyle=style,
            postHashtags=hashtags,
        )
        draft.setDescription()
        description = draft.generatedDescription
    return render(request, '../Frontend/Text-Gen/scripts/index.html', {'description': description})

#GitHubAPI class
class GitHubAPI():
    def authenticate(request):
        client_id = settings.GITHUB_CLIENT_ID
        redirect_uri = settings.GITHUB_REDIRECT_URI
    
        #generates a random string of letters and numbers for security
        state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        #stores state for validation for each session
        request.session['github_state'] = state 
        request.session.save()
        
        print(f"Generated state:{state}")
        github_auth_url = (
            #string literal to generate the url for authentication
            f"https://github.com/login/oauth/authorize?client_id={client_id}"
            f"&redirect_uri={redirect_uri}&state={state}"
        )
        return redirect(github_auth_url)
    
    #url passed in is https://api.github.com/users/USERNAME/repos
    def getUserRepos(auth_token):
        #defines headers
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {auth_token}',
            'X-GitHub-Api-Version': '2022-11-28',
        }

        #retrieves response from api call
        response = requests.get('https://api.github.com/user/repos', headers=headers)

        #ensures correct status code
        if response.status_code == 200:
            repos = response.json()
            public_repos = []
            #fills public_repos with repo data
            for repo in repos:
                if not repo["private"]:
                    public_repos.append({
                        "name": repo["name"],
                        "html_url": repo["html_url"],
                        "description": repo.get("description"),
                        "language": repo.get("language"),
                    })
            return public_repos
        else:
            return {f"error: Failed to fetch repositories - Status Code: {response.status_code}"}
    
    
    def get_access_token(code, state, request):
        token_url = "https://github.com/login/oauth/access_token"
        headers =  {
            'Accept': 'application/json'
        }
        data = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.GITHUB_REDIRECT_URI,
        }
        print(f"Requesting access token with code: {code}")
        print(f"Headers: {headers}")
        print(f"Data: {data}")    
        response = requests.post(token_url, headers=headers, data=data)
        print(f"Token exchange response status: {response.status_code}")
        print(f"Token exchange response body: {response.text}")
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            return {"access_token": access_token}
        else:
            return {"error": "Failed to retrieve access token"}
        
#GithubAPI views
def githubAuth(request):
    return GitHubAPI.authenticate(request)

def fetchUserRepos(request):
    auth_token = request.GET.get('token')
    if not auth_token:
        return JsonResponse({"error": "Authorization token is Incorrect"}, status=400)
    repos = GitHubAPI.get_user_repos(auth_token)
    return JsonResponse(repos, safe=False)

def github_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    session_state = request.session.pop('github_state', None)
    
    #Troubleshooting
    print(f"Github state: {state}")
    print(f"Session State: {session_state}")
    
    if state != session_state:
        return JsonResponse({"error": "Invalid state"}, status=400)
    
    # Use the GitHubAPI class to handle the token exchange
    result = GitHubAPI.get_access_token(code, state, request)
    if "error" in result:
        return JsonResponse(result, status=400)
    
    access_token = result.get('access_token')
    user = request.user
    user_token, created = UserToken.objects.get_or_create(user=user)
    user_token.token = access_token
    user_token.save()
    redirect_url = f"{settings.FRONTEND_REDIRECT_URI}?token={access_token}"

    return HttpResponseRedirect(redirect_url)

def save_draft(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        audience = request.POST.get('audience')
        style = request.POST.get('style')
        tone = request.POST.get('tone')
        hashtags = request.POST.get('hashtags')

        # Save draft to the database
        draft = Draft.objects.create(
            name=name,
            description=description,
            audience=audience,
            style=style,
            tone=tone,
            hashtags=hashtags,
            user=request.user  # Associate draft with the current user
        )

        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
@login_required
def list_drafts(request):
    drafts = Draft.objects.filter(user=request.user).order_by("-created_at")
    drafts_data = drafts.values("id", "name")  # Only sending the id and name to reduce payload size
    return JsonResponse({"drafts": list(drafts_data)})

@login_required
def load_draft(request, draft_id):
    try:
        draft = Draft.objects.get(id=draft_id, user=request.user)  # Make sure we fetch drafts for the current user only
        draft_data = {
            "success": True,
            "draft": {
                "name": draft.name,
                "description": draft.description,
                "audience": draft.audience,
                "style": draft.style,
                "tone": draft.tone,
                "hashtags": draft.hashtags,
            },
        }
        return JsonResponse(draft_data)
    except Draft.DoesNotExist:
        return JsonResponse({"success": False, "message": "Draft not found."}, status=404)

def delete_draft(request, draft_id):
    try:
        draft = Draft.objects.get(id=draft_id, user=request.user)  # Ensure the draft belongs to the current user
        draft.delete()  # Delete the draft
        return JsonResponse({'success': True, 'message': 'Draft deleted successfully.'})
    except Draft.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Draft not found.'}, status=404)
