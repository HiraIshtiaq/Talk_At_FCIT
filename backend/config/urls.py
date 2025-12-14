"""
URL configuration for FCIT Talk project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI schema
schema_view = get_schema_view(
    openapi.Info(
        title="FCIT Talk API",
        default_version='v1',
        description="Academic Discussion Platform for FCIT (PUCIT)",
        contact=openapi.Contact(email="admin@fcit.edu.pk"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/discussions/', include('apps.discussions.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/search/', include('apps.search.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/messaging/', include('apps.messaging.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
