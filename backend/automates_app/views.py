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