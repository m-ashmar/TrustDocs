from django.contrib import admin
from django.urls import path, include  # Add 'include' here

urlpatterns = [
    path("admin/", admin.site.urls),
    # Add these lines to include your app URLs 👇
    path("users/", include("users.urls")),
    path("documents/", include("documents.urls")),
]