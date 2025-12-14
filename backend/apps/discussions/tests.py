"""
Tests for discussions app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.discussions.models import Category, Post, Comment, Vote

User = get_user_model()


class PostTests(TestCase):
    """Test post creation and voting."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@pucit.edu.pk',
            password='TestPass123!',
            is_verified=True
        )
        self.category = Category.objects.create(
            name='General',
            slug='general'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_post(self):
        """Test authenticated user can create post."""
        data = {
            'title': 'Test Post',
            'content': 'This is a test post',
            'category': self.category.id
        }
        response = self.client.post('/api/discussions/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_vote_on_post(self):
        """Test voting on post."""
        post = Post.objects.create(
            author=self.user,
            category=self.category,
            title='Test Post',
            content='Content'
        )
        response = self.client.post(
            f'/api/discussions/posts/{post.id}/vote/',
            {'value': 1}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check vote was recorded
        vote_exists = Vote.objects.filter(user=self.user, post=post).exists()
        self.assertTrue(vote_exists)
