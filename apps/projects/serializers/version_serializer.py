from rest_framework import serializers
from apps.projects.models.version_model import Version

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ["id", "project_id", "version", "upload_id", "is_analysis_complete", "analysis", "ai_summary", "is_active", "created_at", "deleted_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "analysis": {"read_only": True},
            "ai_summary": {"read_only": True},
            "created_at": {"read_only": True}
        }
