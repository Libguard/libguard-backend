from django.contrib import admin
from apps.projects.models.upload_model import Upload

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ("project_id",)
    readonly_fields = ("id", "project_id", "created_at", "expires_at")

    fieldsets = (
        ("Details", {
            "fields": ("id", "project_id")
        }),
        ("Metadata", {
            "fields": ("created_at", "expires_at")
        })
    )