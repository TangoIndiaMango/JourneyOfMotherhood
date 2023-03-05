
from django.urls import path
from .views import CommentCreateView, CommentListView, PostCreateView, PostListView, PostUpdateView, ReactionCreateView, ReactionListView


urlpatterns = [
    path('all/', PostListView.as_view(), name='list_post'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('<pk>/', PostUpdateView.as_view(), name='edit_post'),
    path('<int:post_id>/reaction/', ReactionCreateView.as_view(), name="reaction_post"),
    path('reaction/<int:post_id>/', ReactionListView.as_view(), name="reaction_list"),
    path('<int:post_id>/comment/', CommentCreateView.as_view(), name='comment_post'),
    path('comment/<int:post_id>/', CommentListView.as_view(), name='list_comment'), 
]