"""
User models for FCIT Talk platform.
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError('Email address is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)


def validate_pucit_email(value):
    """Validate that email is from @pucit.edu.pk domain."""
    if not value.endswith('@pucit.edu.pk'):
        raise ValidationError(
            'Only @pucit.edu.pk email addresses are allowed.',
            code='invalid_domain'
        )


class User(AbstractUser):
    """Custom user model with email authentication and FCIT-specific fields."""
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    # Remove username, use email instead
    username = None
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(), validate_pucit_email],
        help_text='Must be a valid @pucit.edu.pk email address'
    )
    
    # Additional fields
    bio = models.TextField(max_length=500, blank=True, default='')
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )
    is_verified = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    suspended_until = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        """Return user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def is_moderator_or_admin(self):
        """Check if user has moderation privileges."""
        return self.role in ['moderator', 'admin']
