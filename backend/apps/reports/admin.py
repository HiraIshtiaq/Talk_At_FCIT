"""
Admin configuration for reports.
"""
from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'report_type', 'status', 'reviewed_by', 'created_at']
    list_filter = ['report_type', 'status', 'created_at']
    search_fields = ['reporter__email', 'reason']
    readonly_fields = ['created_at', 'updated_at']
