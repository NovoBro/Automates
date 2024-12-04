from django.urls import path
from .views import githubAuth, fetchUserRepos, github_callback

urlpatterns = [
    path('auth/', githubAuth, name='github_authenticate'),
    path('repos/', fetchUserRepos, name='fetch_user_repos'),
    path('callback/', github_callback, name='github_callback'),
]
