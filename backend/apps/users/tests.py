"""
Tests for user authentication and registration.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserRegistrationTests(TestCase):
    """Test user registration with email validation."""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/users/'
    
    def test_register_with_valid_email(self):
        """Test registration with @pucit.edu.pk email."""
        data = {
            'email': 'test@pucit.edu.pk',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_register_with_invalid_email(self):
        """Test registration with non-PUCIT email fails."""
        data = {
            'email': 'test@gmail.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAuthenticationTests(TestCase):
    """Test JWT authentication."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@pucit.edu.pk',
            password='TestPass123!',
            first_name='Test',
            last_name='User',
            is_verified=True
        )
        self.login_url = '/api/auth/login/'
    
    def test_login_success(self):
        """Test successful login returns JWT tokens."""
        data = {
            'email': 'test@pucit.edu.pk',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with wrong password fails."""
        data = {
            'email': 'test@pucit.edu.pk',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
