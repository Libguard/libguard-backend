from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import zipfile

class ProjectUplaodSerializer(serializers.Serializer):
    project_path = serializers.FileField()

    def validate_project_path(self, value):
        if not value.name.endswith(".zip"):
            raise ValidationError("The project needs to be compressed into a .zip file.")
        if not zipfile.is_zipfile(value):
            raise ValidationError("Invalid zip file.")
        
        value.seek(0)
        return value
