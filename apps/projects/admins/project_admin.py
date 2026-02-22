from django.contrib import admin
from apps.projects.models.project_model import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "is_active")
    readonly_fields = ("id", "user", "created_at", "deleted_at")

    fieldsets = (
        ("Details", {
            "fields": ("id", "user", "name", "description", "is_active")
        }),
        ("Metadata", {
            "fields": ("created_at", "deleted_at")
        })
    )
