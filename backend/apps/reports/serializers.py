"""
Serializers for reports.
"""
from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for Report model."""
    
    reporter_email = serializers.CharField(source='reporter.email', read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'reporter', 'reporter_email', 'report_type', 'reason',
            'status', 'post_id', 'comment_id', 'reported_user_id',
            'moderator_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reporter', 'status', 'moderator_notes', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Handle custom creation logic if needed, but for now we rely on views
        return super().create(validated_data)
