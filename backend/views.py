from django.http import JsonResponse
from .models import Draft

def generate_description_view(request):
    if request.method == 'POST':
        repo_link = request.POST.get('repoLink')
        user_description = request.POST.get('userDescription')
        audience = request.POST.get('audience')
        tone = request.POST.get('tone')
        style = request.POST.get('style')
        hashtags = request.POST.get('hashtags')

        if not (repo_link and audience and tone and style and hashtags):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
            
        draft = Draft(
            repositoryLink=repo_link,
            userDescription=user_description,
            postAudience=audience,
            postTone=tone,
            postStyle=style,
            postHashtags=hashtags,
        )
        draft.setDescription() 
        return JsonResponse({'description': draft.generatedDescription})

    return JsonResponse({'error': 'Invalid request method'}, status=405)
