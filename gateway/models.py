from django.db import models
from UserProfile.models import CustomUser
# Create your models here.

class JWT(models.Model):
    user = models.OneToOneField(CustomUser, related_name='login_user', on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)