from django.shortcuts import render, redirect
import random
import string
import requests
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings

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