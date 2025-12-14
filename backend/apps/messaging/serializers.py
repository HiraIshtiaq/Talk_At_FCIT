"""
Serializers for messaging app.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, PrivateMessage, ChatRoom, ChatMessage

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user info for messaging context."""
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'profile_picture']


class PrivateMessageSerializer(serializers.ModelSerializer):
    """Serializer for private messages."""
    sender = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = PrivateMessage
        fields = ['id', 'sender', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for conversations."""
    participants = UserMinimalSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    other_participant = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'other_participant', 'last_message', 'unread_count', 'created_at', 'updated_at']
    
    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            return {
                'content': last_msg.content[:100],
                'sender_id': last_msg.sender.id,
                'created_at': last_msg.created_at,
                'is_read': last_msg.is_read
            }
        return None
    
    def get_unread_count(self, obj):
        user = self.context.get('request').user
        return obj.messages.filter(is_read=False).exclude(sender=user).count()
    
    def get_other_participant(self, obj):
        user = self.context.get('request').user
        other = obj.get_other_participant(user)
        if other:
            return UserMinimalSerializer(other).data
        return None


class ConversationDetailSerializer(ConversationSerializer):
    """Detailed conversation with messages."""
    messages = PrivateMessageSerializer(many=True, read_only=True)
    
    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + ['messages']


class CreateMessageSerializer(serializers.Serializer):
    """Serializer for creating a new message."""
    recipient_id = serializers.IntegerField(required=False)
    conversation_id = serializers.IntegerField(required=False)
    content = serializers.CharField()
    
    def validate(self, data):
        if not data.get('recipient_id') and not data.get('conversation_id'):
            raise serializers.ValidationError(
                "Either recipient_id or conversation_id must be provided"
            )
        return data


class ChatRoomSerializer(serializers.ModelSerializer):
    """Serializer for chat rooms."""
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'description', 'is_active', 'message_count', 'created_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages."""
    sender = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'content', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']


class CreateChatMessageSerializer(serializers.Serializer):
    """Serializer for sending a chat message."""
    content = serializers.CharField()
