from django.urls import path
from apps.projects.views import ProjectCreateView

urlpatterns = [
    path("", ProjectCreateView.as_view(), name="create_project")
]
