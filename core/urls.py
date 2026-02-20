from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("upload/", include("apps.dependency_analysis.urls")),
    path('auth/', include("apps.authentication.urls"))
]
