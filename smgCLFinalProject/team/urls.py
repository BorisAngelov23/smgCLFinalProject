from django.urls import path

from smgCLFinalProject.team import views

urlpatterns = [
    path('choose-classes/', views.TeamRegister.as_view(), name='choose_classes'),
    path('add-players/', views.create_multiple_players, name='add_players'),
]
