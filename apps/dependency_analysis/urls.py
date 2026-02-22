from django.urls import path
from apps.dependency_analysis.views import ProjectUploadView

urlpatterns = [
    path("<uuid:project_id>/upload/", ProjectUploadView.as_view(), name="project_upload")
]
