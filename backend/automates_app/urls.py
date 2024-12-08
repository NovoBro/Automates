from django.urls import path, include
from .views import home, authView, accounts, delete_account, githubAuth, fetchUserRepos, github_callback  # Import delete_account view
from .views import save_draft, list_drafts, load_draft, delete_draft

urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    # Include the Django authentication URLs for login, logout, etc.
    path("accounts/", include("django.contrib.auth.urls")),
    # Path for the custom accounts page
    path("accounts/custom/", accounts, name="accounts"),  # Custom route for account page
    path("delete_account/", delete_account, name="delete_account"),  # Path to handle account deletion
    path('auth/', githubAuth, name='github_authenticate'),
    path('repos/', fetchUserRepos, name='fetch_user_repos'),
    path('callback/', github_callback, name='github_callback'), 
    #path('generatedescription/', generatedescription, name='generatedescription'),
    path("save_draft/", save_draft, name="save_draft"),
    path("list_drafts/", list_drafts, name="list_drafts"),
    path("load_draft/<int:draft_id>/", load_draft, name="load_draft"),
    path('delete_draft/<int:draft_id>/', delete_draft, name='delete_draft'),
]
