from rest_framework import serializers
from apps.projects.models.upload_model import Upload
from rest_framework.exceptions import ValidationError
import zipfile

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ["id", "project_id", "created_at", "expires_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "project_id": {"read_only": True},
            "created_at": {"read_only": True},
            "expires_at": {"read_only": True}
        }


    def validate_project_path(self, value):
        if not value.name.endswith(".zip"):
            raise ValidationError("The project needs to be compressed into a .zip file.")
        if not zipfile.is_zipfile(value):
            raise ValidationError("Invalid zip file.")
        
        value.seek(0)
        return value
