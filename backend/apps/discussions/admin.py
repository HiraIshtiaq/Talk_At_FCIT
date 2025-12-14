"""
Admin configuration for discussions app.
"""
from django.contrib import admin
from .models import Category, Post, Comment, Vote


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'upvotes_count', 'comments_count', 'is_pinned', 'created_at']
    list_filter = ['category', 'is_pinned', 'is_locked', 'created_at']
    search_fields = ['title', 'content', 'author__email']
    readonly_fields = ['upvotes_count', 'comments_count', 'created_at', 'updated_at']
    list_editable = ['is_pinned']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post', 'upvotes_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__email']
    readonly_fields = ['upvotes_count', 'created_at', 'updated_at']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'comment', 'value', 'created_at']
    list_filter = ['value', 'created_at']
    search_fields = ['user__email']
