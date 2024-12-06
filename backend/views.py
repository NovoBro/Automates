from django.shortcuts import render
from models import Draft

def generate_description_view(request):
    description = ""
    if request.method == 'POST':
        repo_link = request.POST.get('repositoryLink')
        user_description = request.POST.get('userDescription', "")
        audience = request.POST.get('audience')
        tone = request.POST.get('tone')
        style = request.POST.get('style')
        hashtags = request.POST.get('hashtags')
        draft = Draft(
            repositoryLink=repo_link,
            userDescription=user_description,
            postAudience=audience,
            postTone=tone,
            postStyle=style,
            postHashtags=hashtags,
        )
        draft.setDescription()
        description = draft.generatedDescription
    return render(request, '../Frontend/Text-Gen/scripts/index.html', {'description': description})
