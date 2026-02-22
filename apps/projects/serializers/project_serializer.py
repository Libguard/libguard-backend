from rest_framework import serializers
from apps.projects.models.project_model import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "user", "name", "description", "is_active", "created_at", "deleted_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "created_at": {"read_only": True}
        }
