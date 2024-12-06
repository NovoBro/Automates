'''from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout as auth_logout

# Home page view
def home(request):
    return render(request, "automates_app/home.html")

# Sign up page view
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password = request.POST['password']
        repassword = request.POST['repassword']
        email = request.POST.get('email', '')  # Ensure email field is added in the form

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try some other username")
            return redirect('signup')  # Redirect to signup page if username exists

        # Check if passwords match
        if password != repassword:
            messages.error(request, "Passwords did not match!")
            return redirect('signup')  # Redirect to signup page if passwords don't match

        # Check if username is alphanumeric
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect('signup')  # Redirect to signup page if username is invalid

        # Create new user
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Your account has been successfully created.")
        
        return redirect('login')  # Redirect to login page after successful signup

    return render(request, "automates_app/signup.html")

# Login page view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in successfully!")
            return redirect('home')  # Redirect to the home page or any other page
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('home')  # Redirect back to the login page if login fails

    return render(request, 'automates_app/signin.html')

# Logout view (log the user out)
def logout(request):
    auth_logout(request)  # This will log the user out
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')  # Redirect to home page after logout
'''

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
        if state != request.session.get('github_state'):
            return {"error": "Invalid State"}
        
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
        
        response = requests.post(token_url, headers=headers, data=data)
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

    session_state = request.session.get('github_state')
    
    print(f"Github state: {state}")
    print(f"Session State: {session_state}")
    
    if state != session_state:
        return JsonResponse({"error": "Invalid state"}, status=400)
    
    # Use the GitHubAPI class to handle the token exchange
    result = GitHubAPI.get_access_token(code, state, request)
    if "error" in result:
        return JsonResponse(result, status=400)
    access_token = result.get('access_token')
    redirect_url = f"{settings.FRONTEND_REDIRECT_URI}?token={access_token}"

    return HttpResponseRedirect(redirect_url)