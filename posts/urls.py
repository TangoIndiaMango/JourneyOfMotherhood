
from django.urls import path
from .views import CommentCreateView, CommentListView, PostCreateAPIView, PostDeleteAPIView, PostDetailAPIView, PostListAPIView, PostUpdateAPIView, ReactionCreateView, ReactionListView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions



schema_view = get_schema_view(
    openapi.Info(
        title="Book API",
        default_version='v1',
        description="API for managing books",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@bookapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('<int:post_id>/reaction/',
         ReactionCreateView.as_view(), name="reaction_post"),
    path('reaction/<int:post_id>/',
         ReactionListView.as_view(), name="reaction_list"),
    path('<int:post_id>/comment/', CommentCreateView.as_view(), name='comment_post'),
    path('comment/<int:post_id>/', CommentListView.as_view(), name='list_comment'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path('all/', PostListAPIView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('create/', PostCreateAPIView.as_view(), name='post-create'),
    path('<int:pk>/update/', PostUpdateAPIView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteAPIView.as_view(), name='post-delete'),
]
