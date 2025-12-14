"""
Analytics views for admin dashboard.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from apps.discussions.models import Post, Comment
from apps.reports.models import Report
from apps.users.permissions import IsModeratorOrAdmin

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsModeratorOrAdmin])
def platform_analytics(request):
    """Get platform-wide analytics."""
    
    # Total counts
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    total_comments = Comment.objects.count()
    total_reports = Report.objects.count()
    pending_reports = Report.objects.filter(status='pending').count()
    
    # Active users (posted or commented in last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_users = User.objects.filter(
        Q(posts__created_at__gte=thirty_days_ago) |
        Q(comments__created_at__gte=thirty_days_ago)
    ).distinct().count()
    
    # Posts by category
    posts_by_category = Post.objects.values('category__name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Recent activity (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_posts = Post.objects.filter(created_at__gte=seven_days_ago).count()
    recent_comments = Comment.objects.filter(created_at__gte=seven_days_ago).count()
    recent_users = User.objects.filter(created_at__gte=seven_days_ago).count()
    
    return Response({
        'total_users': total_users,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'total_reports': total_reports,
        'pending_reports': pending_reports,
        'active_users_30d': active_users,
        'posts_by_category': list(posts_by_category),
        'recent_activity': {
            'posts_7d': recent_posts,
            'comments_7d': recent_comments,
            'new_users_7d': recent_users,
        }
    })


@api_view(['GET'])
@permission_classes([IsModeratorOrAdmin])
def user_list_admin(request):
    """Get user list with admin info."""
    users = User.objects.annotate(
        posts_count=Count('posts'),
        comments_count=Count('comments')
    ).order_by('-created_at')
    
    # Filters
    role = request.query_params.get('role')
    if role:
        users = users.filter(role=role)
    
    is_suspended = request.query_params.get('is_suspended')
    if is_suspended:
        users = users.filter(is_suspended=True)
    
    data = [{
        'id': user.id,
        'email': user.email,
        'full_name': user.full_name,
        'role': user.role,
        'is_verified': user.is_verified,
        'is_suspended': user.is_suspended,
        'posts_count': user.posts_count,
        'comments_count': user.comments_count,
        'created_at': user.created_at,
    } for user in users[:100]]  # Limit to 100
    
    return Response({'users': data, 'count': users.count()})


@api_view(['POST'])
@permission_classes([IsModeratorOrAdmin])
def suspend_user(request, user_id):
    """Suspend or unsuspend a user."""
    try:
        user = User.objects.get(id=user_id)
        action = request.data.get('action')  # 'suspend' or 'unsuspend'
        
        if action == 'suspend':
            user.is_suspended = True
            user.save()
            return Response({'message': f'User {user.email} suspended'})
        elif action == 'unsuspend':
            user.is_suspended = False
            user.suspended_until = None
            user.save()
            return Response({'message': f'User {user.email} unsuspended'})
        else:
            return Response({'error': 'Invalid action'}, status=400)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
