from django.urls import path
from apps.dependency_analysis.views import ProjectUploadView

urlpatterns = [
    path("", ProjectUploadView.as_view(), name="project_upload")
]
