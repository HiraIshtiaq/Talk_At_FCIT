"""
Django signals for creating notifications.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.discussions.models import Comment, Vote
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Create notification when someone comments on a post."""
    if not created:
        return
    
    # Notify post author
    if instance.author != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.author,
            notification_type='comment',
            message=f"{instance.author.full_name} commented on your post: {instance.post.title}",
            post_id=instance.post.id,
            comment_id=instance.id
        )
        
        # Send real-time notification
        send_realtime_notification(instance.post.author.id)
    
    # Notify parent comment author (if reply)
    if instance.parent and instance.author != instance.parent.author:
        Notification.objects.create(
            recipient=instance.parent.author,
            sender=instance.author,
            notification_type='reply',
            message=f"{instance.author.full_name} replied to your comment",
            post_id=instance.post.id,
            comment_id=instance.id
        )
        
        send_realtime_notification(instance.parent.author.id)


def send_realtime_notification(user_id):
    """Send real-time notification via WebSocket."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user_id}',
        {
            'type': 'notification_message',
            'message': 'You have a new notification'
        }
    )
