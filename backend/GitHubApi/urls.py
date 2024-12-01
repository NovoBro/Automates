from django.urls import path
from .views import github_authenticate, fetch_user_repos

urlpatterns = [
    path('auth/', github_authenticate, name='github_authenticate'),
    path('repos/', fetch_user_repos, name='fetch_user_repos'),
]
