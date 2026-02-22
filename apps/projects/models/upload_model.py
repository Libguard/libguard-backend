from django.db import models
from .project_model import Project

class Upload(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    expires_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        verbose_name = "Upload"
        verbose_name_plural = "Uploads"


    def __str__(self) -> str:
        return f"Project ID: {self.project_id}"
