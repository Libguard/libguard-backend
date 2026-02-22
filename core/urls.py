from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.dependency_analysis.urls")),
    path("create-project/", include("apps.projects.urls")),
    path('auth/', include("apps.authentication.urls")),
]
