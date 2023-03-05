from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post, Reaction, Comment
from .serializers import CommentSerializer, PostSerializer, ReactionSerializer

# Create your views here.


class PostPagination(PageNumberPagination):
    page_size = 15
    page_query_param = page_size
    max_page_size = 50


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination


class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author == request.user:
            return self.update(request, *args, **kwargs)
        else:
            return Response({'detail': 'You do not have permission to edit this post.'}, status=status.HTTP_403_FORBIDDEN)


# class ReactionCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, post_id):
#         try:
#             post = Post.objects.get(pk=post_id)
#         except Post.DoesNotExist:
#             return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

#         reaction_type = request.data.get('reaction_type')
#         if not reaction_type:
#             return Response({'detail': 'Missing reaction_type field.'}, status=status.HTTP_400_BAD_REQUEST)

#         reaction = Reaction.objects.filter(
#             post=post, user=request.user).first()
#         if reaction:
#             reaction.reaction_type = reaction_type
#             reaction.save()
#         else:
#             reaction = Reaction.objects.create(
#                 post=post, user=request.user, reaction_type=reaction_type)

#         return Response({'detail': 'Reaction added.'}, status=status.HTTP_201_CREATED)

class ReactionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response({'detail': 'Reaction added.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReactionListView(ListAPIView):
    serializer_class = ReactionSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Reaction.objects.filter(post=post_id)
        return queryset


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post=post_id)
        return queryset
