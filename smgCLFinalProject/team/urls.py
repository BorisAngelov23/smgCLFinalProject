from django.urls import path

from smgCLFinalProject.team import views

urlpatterns = [
    path("team/choose-classes/", views.TeamRegister.as_view(), name="choose_classes"),
    path("team/add-players/", views.players_add, name="add_players"),
    path("team/management/edit/", views.players_edit, name="players_edit"),
    path("team/management/add-more-players/", views.player_add,
         name="players_extra_add"),
    path("team-standings/", views.Standings.as_view(), name="standings"),
    path("player-standings/", views.PlayerStandings.as_view(),
         name="player_standings"),
    path("team/<int:pk>/", views.PlayersFromTeam.as_view(),
         name="players_from_team"),
    path("player/<int:pk>/", views.PlayerDetail.as_view(), name="player_detail"),
    path("team/management/", views.TeamManagement.as_view(), name="team_management"),
]
