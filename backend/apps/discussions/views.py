"""
Views for discussions app.
"""
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes as perm_classes
from rest_framework.response import Response
from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from .models import Category, Post, Comment, Vote
from .serializers import (
    CategorySerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostCreateSerializer,
    CommentSerializer,
)
from apps.users.permissions import IsModeratorOrAdmin


class CategoryListView(generics.ListCreateAPIView):
    """List all categories or create new one (admin only)."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsModeratorOrAdmin()]
        return [permissions.AllowAny()]


class PostListCreateView(generics.ListCreateAPIView):
    """List all posts or create new post."""
    
    queryset = Post.objects.select_related('author', 'category').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'author__first_name', 'author__last_name']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by author
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__id=author)
        
        # Ordering
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering == 'popular':
            queryset = queryset.order_by('-upvotes_count', '-created_at')
        elif ordering == 'trending':
            # Simple trending: high upvotes + recent
            queryset = queryset.order_by('-upvotes_count', '-comments_count', '-created_at')
        else:
            queryset = queryset.order_by(ordering)
        
        return queryset


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a post."""
    
    queryset = Post.objects.select_related('author', 'category').all()
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_update(self, serializer):
        # Only author or moderator can update
        user = self.request.user
        if self.get_object().author != user and user.role not in ['admin', 'moderator']:
             raise serializers.ValidationError({'error': 'Permission denied'})
        serializer.save()
    
    def perform_destroy(self, instance):
        # Only author or moderator can delete
        user = self.request.user
        if instance.author != user and user.role not in ['admin', 'moderator']:
            raise serializers.ValidationError({'error': 'Permission denied'})
        instance.delete()


class CommentListCreateView(generics.ListCreateAPIView):
    """List comments for a post or create new comment."""
    
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).select_related('author')
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        if post.is_locked and not self.request.user.is_moderator_or_admin():
            raise serializers.ValidationError("This post is locked.")
        
        serializer.save(author=self.request.user, post=post)
        
        # Update comment count
        Post.objects.filter(id=post.id).update(comments_count=F('comments_count') + 1)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a comment."""
    
    queryset = Comment.objects.select_related('author').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.author != self.request.user and not self.request.user.is_moderator_or_admin():
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        post = instance.post
        instance.delete()
        
        # Update post comment count
        Post.objects.filter(id=post.id).update(comments_count=F('comments_count') - 1)


@api_view(['POST'])
@perm_classes([permissions.IsAuthenticated])
def vote_post(request, post_id):
    """Upvote or downvote a post."""
    post = get_object_or_404(Post, id=post_id)
    value = request.data.get('value')
    
    if value not in [1, -1]:
        return Response({'error': 'Invalid vote value'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user already voted
    vote, created = Vote.objects.get_or_create(
        user=request.user,
        post=post,
        defaults={'value': value}
    )
    
    if not created:
        if vote.value == value:
            # Remove vote
            vote.delete()
            Post.objects.filter(id=post_id).update(upvotes_count=F('upvotes_count') - value)
            return Response({'message': 'Vote removed'}, status=status.HTTP_200_OK)
        else:
            # Change vote
            old_value = vote.value
            vote.value = value
            vote.save()
            Post.objects.filter(id=post_id).update(upvotes_count=F('upvotes_count') - old_value + value)
            return Response({'message': 'Vote updated'}, status=status.HTTP_200_OK)
    else:
        # New vote
        Post.objects.filter(id=post_id).update(upvotes_count=F('upvotes_count') + value)
        return Response({'message': 'Vote recorded'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@perm_classes([permissions.IsAuthenticated])
def vote_comment(request, comment_id):
    """Upvote or downvote a comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    value = request.data.get('value')
    
    if value not in [1, -1]:
        return Response({'error': 'Invalid vote value'}, status=status.HTTP_400_BAD_REQUEST)
    
    vote, created = Vote.objects.get_or_create(
        user=request.user,
        comment=comment,
        defaults={'value': value}
    )
    
    if not created:
        if vote.value == value:
            vote.delete()
            Comment.objects.filter(id=comment_id).update(upvotes_count=F('upvotes_count') - value)
            return Response({'message': 'Vote removed'}, status=status.HTTP_200_OK)
        else:
            old_value = vote.value
            vote.value = value
            vote.save()
            Comment.objects.filter(id=comment_id).update(upvotes_count=F('upvotes_count') - old_value + value)
            return Response({'message': 'Vote updated'}, status=status.HTTP_200_OK)
    else:
        Comment.objects.filter(id=comment_id).update(upvotes_count=F('upvotes_count') + value)
        return Response({'message': 'Vote recorded'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def trending_posts(request):
    """Get trending posts."""
    posts = Post.objects.select_related('author', 'category').order_by(
        '-upvotes_count', '-comments_count', '-created_at'
    )[:10]
    
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)
