import requests
import random
import string
from django.conf import settings

class GitHubAPI():
    def authenticate(request):
        client_id = settings.GITHUB_CLIENT_ID
        redirect_uri = settings.GITHUB_REDIRECT_URI
    
        #generates a random string of letters and numbers for security
        state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        #stores state for validation for each session
        request.session['github_state'] = state 
        
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
            'Authorization': 'Bearer <YOUR-TOKEN>',
            'X-GitHub-Api-Version': '2022-11-28',
        }

        #retrieves response from api call
        response = requests.get('https://api.github.com/user/repos', headers = headers)

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
