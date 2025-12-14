"""
Models for discussions: Category, Post, Comment, Vote.
"""
from django.db import models
from django.conf import settings
# from django.contrib.postgres.search import SearchVectorField
# from django.contrib.postgres.indexes import GinIndex


class Category(models.Model):
    """Discussion categories."""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """Discussion posts."""
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    # Full-text search (PostgreSQL only - commented for SQLite)
    # search_vector = SearchVectorField(null=True, blank=True)
    
    # Counters (denormalized for performance)
    upvotes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    
    # Flags
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
        indexes = [
            # GinIndex(fields=['search_vector']),  # PostgreSQL only
            models.Index(fields=['-created_at']),
            models.Index(fields=['-upvotes_count']),
        ]
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    """Comments on posts."""
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    # Counters
    upvotes_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at']),
        ]
    
    def __str__(self):
        return f"Comment by {self.author.email} on {self.post.title}"


class Vote(models.Model):
    """Votes on posts and comments."""
    
    VOTE_CHOICES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='votes'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='votes'
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'votes'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_user_post_vote',
                condition=models.Q(post__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['user', 'comment'],
                name='unique_user_comment_vote',
                condition=models.Q(comment__isnull=False)
            ),
            models.CheckConstraint(
                check=(
                    models.Q(post__isnull=False, comment__isnull=True) |
                    models.Q(post__isnull=True, comment__isnull=False)
                ),
                name='vote_on_post_or_comment'
            ),
        ]
    
    def __str__(self):
        target = self.post or self.comment
        return f"{self.user.email} voted {self.value} on {target}"
