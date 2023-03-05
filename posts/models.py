from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        self.user.post_count += 1
        self.user.save()


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
