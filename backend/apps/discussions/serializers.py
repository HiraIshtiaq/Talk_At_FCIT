"""
Serializers for discussions app.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Post, Comment, Vote
from apps.users.serializers import UserListSerializer

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_posts_count(self, obj):
        return obj.posts.count()


class PostListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for post lists."""
    
    author = UserListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    user_vote = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'author', 'category', 'category_name',
            'upvotes_count', 'comments_count', 'is_pinned',
            'user_vote', 'created_at', 'updated_at'
        ]

    def get_user_vote(self, obj):
        """Get current user's vote on this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            vote = Vote.objects.filter(user=request.user, post=obj).first()
            return vote.value if vote else None
        return None


class PostDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual posts."""
    
    author = UserListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    user_vote = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'category', 'category_name',
            'upvotes_count', 'comments_count', 'is_pinned', 'is_locked',
            'user_vote', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'upvotes_count', 'comments_count', 'created_at', 'updated_at']
    
    def get_user_vote(self, obj):
        """Get current user's vote on this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            vote = Vote.objects.filter(user=request.user, post=obj).first()
            return vote.value if vote else None
        return None


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts."""
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""
    
    author = UserListSerializer(read_only=True)
    user_vote = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'content', 'parent',
            'upvotes_count', 'replies_count', 'user_vote',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'post', 'upvotes_count', 'created_at', 'updated_at']
    
    def get_user_vote(self, obj):
        """Get current user's vote on this comment."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            vote = Vote.objects.filter(user=request.user, comment=obj).first()
            return vote.value if vote else None
        return None
    
    def get_replies_count(self, obj):
        return obj.replies.count()


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for votes."""
    
    class Meta:
        model = Vote
        fields = ['id', 'post', 'comment', 'value', 'created_at']
        read_only_fields = ['id', 'created_at']
