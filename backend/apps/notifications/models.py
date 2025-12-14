"""
Notification models.
"""
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """User notifications."""
    
    NOTIFICATION_TYPES = [
        ('comment', 'New Comment'),
        ('reply', 'Reply to Comment'),
        ('mention', 'Mention'),
        ('vote', 'Vote on Post/Comment'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        null=True,
        blank=True
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    
    # Links to related objects
    post_id = models.IntegerField(null=True, blank=True)
    comment_id = models.IntegerField(null=True, blank=True)
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]
    
    def __str__(self):
        return f"Notification for {self.recipient.email}: {self.notification_type}"
