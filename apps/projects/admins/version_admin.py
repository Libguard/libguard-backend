from django.contrib import admin
from apps.projects.models.version_model import Version

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("project_id", "version", "is_analysis_complete", "is_active")
    readonly_fields = ("project_id", "upload_id", "is_analysis_complete", "analysis", "ai_summary", "created_at", "deleted_at")

    fieldsets = (
        ("Details", {
            "fields": ("project_id", "version", "upload_id", "is_analysis_complete", "analysis", "ai_summary")
        }),
        ("Metadata", {
            "fields": ("is_active", "created_at", "deleted_at")
        })
    )