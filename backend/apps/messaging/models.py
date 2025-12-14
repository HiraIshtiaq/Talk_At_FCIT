"""
Models for messaging: private conversations and general chat.
"""
from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """Private conversation between two users."""
    
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversation {self.id}"
    
    def get_other_participant(self, user):
        """Get the other participant in a two-person conversation."""
        return self.participants.exclude(id=user.id).first()


class PrivateMessage(models.Model):
    """Private message within a conversation."""
    
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'private_messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.email} at {self.created_at}"


class ChatRoom(models.Model):
    """General chat room for group conversations."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chat_rooms'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    """Message in a chat room."""
    
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['room', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.sender.email} in {self.room.name}: {self.content[:50]}"
