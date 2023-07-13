from django.urls import path

from smgCLFinalProject.team import views

urlpatterns = [
    path('register/', views.TeamRegister.as_view(), name='team_register'),
]
