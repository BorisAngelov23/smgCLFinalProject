from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("smgCLFinalProject.core.urls")),
    path("", include("smgCLFinalProject.auth_app.urls")),
    path("", include("smgCLFinalProject.team.urls")),
    path("matches/", include("smgCLFinalProject.match.urls")),
    path("news/", include("smgCLFinalProject.article.urls")),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="auth_app/password_reset.html"
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="auth_app/password_reset_sent.html"
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="auth_app/password_reset_confirm.html"
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="auth_app/password_reset_complete.html"
    ), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
