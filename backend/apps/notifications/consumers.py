"""
WebSocket consumer for real-time notifications.
"""
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for user notifications."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.user = self.scope['user']
        
        if self.user.is_anonymous:
            await self.close()
            return
        
        self.group_name = f'notifications_{self.user.id}'
        
        # Join notification group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def notification_message(self, event):
        """Receive notification from group and send to WebSocket."""
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
