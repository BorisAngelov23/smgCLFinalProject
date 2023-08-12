from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('smgCLFinalProject.core.urls')),
    path('', include('smgCLFinalProject.auth_app.urls')),
    path('', include('smgCLFinalProject.team.urls')),
    path('matches/', include('smgCLFinalProject.match.urls')),
    path('news/', include('smgCLFinalProject.article.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
