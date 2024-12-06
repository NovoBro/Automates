from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# UserToken store
class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Associate the token with a user
    token = models.TextField()  # Store the token
    created_at = models.DateTimeField(auto_now_add=True)  # Track when the token was created

    def __str__(self):
        return f"Token for {self.user.username}"