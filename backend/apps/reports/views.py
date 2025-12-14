"""
Views for content reporting.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes as perm_classes
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
from apps.users.permissions import IsModeratorOrAdmin


class ReportCreateView(generics.CreateAPIView):
    """Create a new report."""
    
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class ReportListView(generics.ListAPIView):
    """List all reports (moderators only)."""
    
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsModeratorOrAdmin]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


@api_view(['POST'])
@perm_classes([IsModeratorOrAdmin])
def update_report_status(request, pk):
    """Update report status (moderators only)."""
    try:
        report = Report.objects.get(pk=pk)
        new_status = request.data.get('status')
        moderator_notes = request.data.get('moderator_notes', '')
        
        if new_status not in ['pending', 'reviewed', 'resolved', 'dismissed']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        report.status = new_status
        report.moderator_notes = moderator_notes
        report.reviewed_by = request.user
        report.save()
        
        return Response({'message': 'Report updated'}, status=status.HTTP_200_OK)
    except Report.DoesNotExist:
        return Response({'error': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)
