from django.dispatch import receiver
from django.db import models

from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()



class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='post_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title


@receiver(post_save, sender=Post)
def update_user_profile_post_count(sender, instance, created, **kwargs):
    if created and instance.author is not None:
        instance.author.post_count += 1
        instance.author.save()


class Reaction(models.Model):
    INSIGHTFUL = 'insightful'
    SUPPORT = 'support'
    SURPRISE = 'surprise'
    SAD = 'sad'
    LOVE = 'love'
    ANGER = 'anger'
    LIKE = 'like'
    REACTION_TYPES = [
        (INSIGHTFUL, 'Insightful'),
        (SUPPORT, 'Support'),
        (SURPRISE, 'Surprise'),
        (SAD, 'Sad'),
        (LOVE, 'Love'),
        (ANGER, 'Anger'),
        (LIKE, 'Like'),
    ]

    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(choices=REACTION_TYPES, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['post', 'user']

    def __str__(self):
        return f"{self.reaction_type} on {self.post}"


class Comment(models.Model):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment on {self.post}: {self.text[:50]}"
