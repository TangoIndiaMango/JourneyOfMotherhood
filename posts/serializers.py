from rest_framework import serializers

from UserProfile.serializers import UserProfileSerializer
from .models import Comment, Post, Reaction


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'updated_at']


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    tags = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    views = serializers.IntegerField(read_only=True)
    # topic = serializers.CharField(max_length=3)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'author',
                  'created_at', 'updated_at', 'tags', 'image', 'views', 'topic')


class AnonymousPostSerializer(serializers.ModelSerializer):
    tags = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    views = serializers.IntegerField(read_only=True)
    # topic = serializers.CharField(max_length=3)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description',
                  'tags', 'image', 'views', 'topic')
