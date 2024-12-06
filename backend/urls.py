from django.urls import path
from .views import githubAuth, fetchUserRepos, github_callback, generate_description_view

urlpatterns = [
    path('auth/', githubAuth, name='github_authenticate'),
    path('repos/', fetchUserRepos, name='fetch_user_repos'),
    path('callback/', github_callback, name='github_callback'),
    path('generate-description/', generate_description_view, name='generate_description')
]
