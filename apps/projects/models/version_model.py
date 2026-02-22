from django.db import models
from .project_model import Project
from .upload_model import Upload

class Version(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    version = models.CharField(max_length=200, default="1.0.0", null=False, blank=False)
    upload_id = models.ForeignKey(Upload, on_delete=models.CASCADE)
    is_analysis_complete = models.BooleanField(default=False, null=False, blank=False)
    analysis = models.JSONField(null=False, blank=False)
    ai_summary = models.TextField(default="", null=False, blank=False) # Depois que tiver a IA generativa, pode tirar o 'default=""'
    is_active = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)


    class Meta:
        verbose_name = "Version"
        verbose_name_plural = "Versions"


    def __str__(self) -> str:
        return f"Version: {self.version}"
