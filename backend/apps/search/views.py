"""
Search views using simple text search (SQLite compatible).
For PostgreSQL full-text search, see commented code below.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from apps.discussions.models import Post
from apps.discussions.serializers import PostListSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_posts(request):
    """Search posts using simple text search (SQLite compatible)."""
    query = request.query_params.get('q', '')
    
    if not query:
        return Response({'results': []})
    
    # Simple text search (works with SQLite)
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ).order_by('-created_at')
    
    # PostgreSQL full-text search (uncomment when using PostgreSQL)
    # search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
    # search_query = SearchQuery(query)
    # posts = Post.objects.annotate(
    #     rank=SearchRank(search_vector, search_query)
    # ).filter(rank__gte=0.01).order_by('-rank')
    
    # Apply filters
    category = request.query_params.get('category')
    if category:
        posts = posts.filter(category__slug=category)
    
    # Pagination
    page_size = 20
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size
    
    serializer = PostListSerializer(posts[start:end], many=True)
    
    return Response({
        'results': serializer.data,
        'count': posts.count(),
        'page': page
    })
