from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden, JsonResponse
from .models import Draft
from django.http import JsonResponse

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

def save_draft(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        audience = request.POST.get('audience')
        style = request.POST.get('style')
        tone = request.POST.get('tone')
        hashtags = request.POST.get('hashtags')

        # Save draft to the database
        draft = Draft.objects.create(
            name=name,
            description=description,
            audience=audience,
            style=style,
            tone=tone,
            hashtags=hashtags,
            user=request.user  # Associate draft with the current user
        )

        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
@login_required
def list_drafts(request):
    drafts = Draft.objects.filter(user=request.user).order_by("-created_at")
    drafts_data = drafts.values("id", "name")  # Only sending the id and name to reduce payload size
    return JsonResponse({"drafts": list(drafts_data)})

@login_required
def load_draft(request, draft_id):
    try:
        draft = Draft.objects.get(id=draft_id, user=request.user)  # Make sure we fetch drafts for the current user only
        draft_data = {
            "success": True,
            "draft": {
                "name": draft.name,
                "description": draft.description,
                "audience": draft.audience,
                "style": draft.style,
                "tone": draft.tone,
                "hashtags": draft.hashtags,
            },
        }
        return JsonResponse(draft_data)
    except Draft.DoesNotExist:
        return JsonResponse({"success": False, "message": "Draft not found."}, status=404)

def delete_draft(request, draft_id):
    try:
        draft = Draft.objects.get(id=draft_id, user=request.user)  # Ensure the draft belongs to the current user
        draft.delete()  # Delete the draft
        return JsonResponse({'success': True, 'message': 'Draft deleted successfully.'})
    except Draft.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Draft not found.'}, status=404)
