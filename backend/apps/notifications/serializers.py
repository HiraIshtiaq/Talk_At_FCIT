"""
Serializers for notifications.
"""
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""
    
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'message', 'sender_name',
            'post_id', 'comment_id', 'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
