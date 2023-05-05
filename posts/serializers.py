from rest_framework import serializers

from UserProfile.serializers import UserProfileSerializer
from .models import Comment, Post, Reaction


class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'created_at', 'updated_at']


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(required=False)
    tags = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    views = serializers.IntegerField(read_only=True)
    # topic = serializers.CharField(max_length=3)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'author', 'user',
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

class PopularTopicSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ['topic', 'count']
        

class TrendingPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'views')


class NewPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'created_at')