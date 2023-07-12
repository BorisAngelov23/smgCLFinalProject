from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('smgCLFinalProject.core.urls')),
    path('accounts/', include('smgCLFinalProject.auth_app.urls')),
]
