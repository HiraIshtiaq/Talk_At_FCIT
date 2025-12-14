from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q
from django.contrib.auth import get_user_model
from apps.users.serializers import UserListSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_users(request):
    """Search users for chat."""
    query = request.query_params.get('q', '')
    
    if not query:
        return Response({'results': []})
    
    users = User.objects.filter(
        Q(email__icontains=query) | 
        Q(first_name__icontains=query) | 
        Q(last_name__icontains=query)
    ).exclude(id=request.user.id)[:10]  # Exclude self
    
    serializer = UserListSerializer(users, many=True)
    
    return Response({'results': serializer.data})
