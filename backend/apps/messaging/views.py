"""
Views for messaging app.
"""
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Q, Max
from .models import Conversation, PrivateMessage, ChatRoom, ChatMessage
from .serializers import (
    ConversationSerializer, ConversationDetailSerializer,
    PrivateMessageSerializer, CreateMessageSerializer,
    ChatRoomSerializer, ChatMessageSerializer, CreateChatMessageSerializer
)

User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversations."""
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
        ).annotate(
            last_message_time=Max('messages__created_at')
        ).order_by('-last_message_time')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Mark messages as read
        instance.messages.filter(is_read=False).exclude(
            sender=request.user
        ).update(is_read=True)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def start(self, request):
        """Start a new conversation or get existing one."""
        recipient_id = request.data.get('recipient_id')
        
        if not recipient_id:
            return Response(
                {'error': 'recipient_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check for existing conversation
        existing = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=recipient
        ).first()
        
        if existing:
            serializer = ConversationDetailSerializer(
                existing, context={'request': request}
            )
            return Response(serializer.data)
        
        # Create new conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, recipient)
        
        serializer = ConversationDetailSerializer(
            conversation, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SendMessageView(generics.CreateAPIView):
    """View for sending a private message."""
    serializer_class = CreateMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        conversation_id = serializer.validated_data.get('conversation_id')
        recipient_id = serializer.validated_data.get('recipient_id')
        content = serializer.validated_data['content']
        
        if conversation_id:
            try:
                conversation = Conversation.objects.get(
                    id=conversation_id,
                    participants=request.user
                )
            except Conversation.DoesNotExist:
                return Response(
                    {'error': 'Conversation not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Find or create conversation with recipient
            try:
                recipient = User.objects.get(id=recipient_id)
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            conversation = Conversation.objects.filter(
                participants=request.user
            ).filter(
                participants=recipient
            ).first()
            
            if not conversation:
                conversation = Conversation.objects.create()
                conversation.participants.add(request.user, recipient)
        
        # Create message
        message = PrivateMessage.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        
        # Update conversation timestamp
        conversation.save()  # This updates updated_at
        
        return Response(
            PrivateMessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )


class ChatRoomViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for chat rooms."""
    queryset = ChatRoom.objects.filter(is_active=True)
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get messages for a chat room."""
        room = self.get_object()
        messages = room.messages.order_by('-created_at')[:100]
        serializer = ChatMessageSerializer(reversed(list(messages)), many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Send a message to a chat room."""
        room = self.get_object()
        serializer = CreateChatMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        message = ChatMessage.objects.create(
            room=room,
            sender=request.user,
            content=serializer.validated_data['content']
        )
        
        return Response(
            ChatMessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
