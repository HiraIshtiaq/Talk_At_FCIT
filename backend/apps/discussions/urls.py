"""
URL patterns for discussions app.
"""
from django.urls import path
from .views import (
    CategoryListView,
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    CommentDetailView,
    vote_post,
    vote_comment,
    trending_posts,
)

app_name = 'discussions'

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    
    # Posts
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/trending/', trending_posts, name='post-trending'),
    path('posts/<int:post_id>/vote/', vote_post, name='post-vote'),
    
    # Comments
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<int:comment_id>/vote/', vote_comment, name='comment-vote'),
]
