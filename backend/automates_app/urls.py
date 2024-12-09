from django.urls import path, include
from .views import home, authView, accounts, delete_account, githubAuth, fetchUserRepos, github_callback
from .views import save_draft, list_drafts, load_draft, delete_draft, generate_description

urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/custom/", accounts, name="accounts"),  
    path("delete_account/", delete_account, name="delete_account"),  
    path('auth/', githubAuth, name='github_authenticate'),
    path('repos/', fetchUserRepos, name='fetch_user_repos'),
    path('callback/', github_callback, name='github_callback'), 
    path('generate_description/', generate_description, name='generate_description'),
    path("save_draft/", save_draft, name="save_draft"),
    path("list_drafts/", list_drafts, name="list_drafts"),
    path("load_draft/<int:draft_id>/", load_draft, name="load_draft"),
    path('delete_draft/<int:draft_id>/', delete_draft, name='delete_draft'),
]
