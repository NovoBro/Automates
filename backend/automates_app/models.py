from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
'''
# Draft corresponds to a project in the ERD
class Draft(models.Model):
    repository_link = models.URLField(max_length=255)
    user_description = models.TextField()
    post_audience = models.CharField(max_length=50)
    post_tone = models.CharField(max_length=50)
    post_style = models.CharField(max_length=50)
    post_hashtags = models.TextField()
    ai_prompt = models.TextField()
    generated_description = models.TextField(null=True, blank=True)
    date_uploaded = models.DateField(auto_now_add=True)
    time_uploaded = models.TimeField(auto_now_add=True)
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="drafts")

    def validate_post_completion(self):
        return bool(self.repository_link and (self.generated_description or self.user_description))


# Post corresponds to the Post entity in the ERD
class Post(models.Model):
    description = models.TextField()
    generated_text = models.TextField()  # To represent Generated/Text (AI Edited)
    generated_image = models.ImageField(upload_to="posts/images/", null=True, blank=True)  # To represent GeneratedImage
    date_generated = models.DateField(auto_now_add=True)
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="posts")

    def fill_from_draft(self, draft):
        self.description = draft.generated_description or draft.user_description
        self.generated_text = draft.ai_prompt
        self.date_generated = draft.date_uploaded
        self.save()


# UserProfile corresponds to the User entity in the ERD
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    linkedin_username = models.CharField(max_length=150, null=True, blank=True)
    linkedin_access_token = models.TextField(null=True, blank=True)
    github_username = models.CharField(max_length=150, null=True, blank=True)
    github_access_token = models.TextField(null=True, blank=True)
    x_username = models.CharField(max_length=150, null=True, blank=True)  # 'X' (formerly Twitter)
    x_access_token = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def post_to_linkedin(self, draft):
        post = Post()
        post.fill_from_draft(draft)
        # Logic for LinkedIn posting API (mocked here)
        # success = LinkedInAPI.post(post.description, self.linkedin_access_token)
        success = True  # Placeholder for LinkedIn posting success
        if success:
            post.user = self
            post.save()
            draft.delete()
            return True
        return False
'''