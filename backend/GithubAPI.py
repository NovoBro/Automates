from django.db import models
import requests
import random
import string
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings

class GitHubAPI():
    def authenticate(request):
        client_id = settings.GITHUB_CLIENT_ID
        redirect_uri = settings.GITHUB_REDIRECT_URI
    
        #generates a random string of letters and numbers for security
        state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
        github_auth_url = (
            #string literal to generate the url for authentication
            f"https://github.com/login/oauth/authorize?client_id={client_id}"
            f"&redirect_uri={redirect_uri}&state={state}"
        )
        return redirect(github_auth_url)
    
    #WIP
    def getUserrepositories():
        return
    
    #WIP
    def getRepoDetails():
        return