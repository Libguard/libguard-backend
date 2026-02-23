from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.projects.serializers.project_serializer import ProjectSerializer

class ProjectCreateView(CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
