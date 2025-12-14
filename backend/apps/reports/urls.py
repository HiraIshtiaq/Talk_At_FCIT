"""
URL patterns for reports app.
"""
from django.urls import path
from .views import ReportCreateView, ReportListView, update_report_status

app_name = 'reports'

urlpatterns = [
    path('', ReportListView.as_view(), name='report-list'),
    path('create/', ReportCreateView.as_view(), name='report-create'),
    path('<int:pk>/update/', update_report_status, name='report-update'),
]
