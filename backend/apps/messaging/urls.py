"""
URL configuration for messaging app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, SendMessageView, ChatRoomViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'chat-rooms', ChatRoomViewSet, basename='chatroom')

urlpatterns = [
    path('', include(router.urls)),
    path('send/', SendMessageView.as_view(), name='send-message'),
]
