from rest_framework.generics import CreateAPIView
from apps.projects.serializers.project_serializer import ProjectSerializer

class ProjectCreateView(CreateAPIView):
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
