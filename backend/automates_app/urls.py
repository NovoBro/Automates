"""
URL configuration for Automates project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
]   
"""
from django.urls import path, include
from .views import home, authView, accounts, delete_account, githubAuth, fetchUserRepos, github_callback  # Import delete_account view

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
]
