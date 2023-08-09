from django.urls import path
from . import views
from smgCLFinalProject.team import views as team_views

urlpatterns = [
    path('register/', views.CaptainRegister.as_view(), name='captain_register'),
    path('login/', views.CaptainLogin.as_view(), name='captain_login'),
    path('logout/', views.CaptainLogout.as_view(), name='captain_logout'),
    path('profile/details/<int:pk>', views.CaptainDetails.as_view(), name='captain_details'),
    path('profile/edit/<int:pk>', views.CaptainEdit.as_view(), name='captain_edit'),
    path('team/edit/', team_views.players_edit, name='players_edit'),
    path('team/add-more-players/', team_views.AddPlayer.as_view(), name='players_extra_add'),
]
