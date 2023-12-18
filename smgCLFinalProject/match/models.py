from django.db import models

from smgCLFinalProject.auth_app.models import CaptainUser
from smgCLFinalProject.team.models import Team, Player


class Match(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
        ("live", "Live"),
        ("played", "Played"),
    )

    RESPONSE_CHOICES = (
        ("accepted", "Accept"),
        ("declined", "Decline"),
    )

    date = models.DateField()
    time = models.TimeField()
    team1 = models.ForeignKey(
        Team, related_name="team1_matches", on_delete=models.CASCADE
    )
    team2 = models.ForeignKey(
        Team, related_name="team2_matches", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending")
    team1_goals = models.IntegerField(null=True, blank=True)
    team2_goals = models.IntegerField(null=True, blank=True)
    mvp = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="match_mvp",
    )
    player_stats = models.ManyToManyField(
        Player, through="MatchPlayerStats", related_name="match_player_stats"
    )

    def update_players(self):
        for player in self.team1.players.all():
            player.mvps = Match.objects.filter(mvp=player).count()
            player.games_played = (
                Match.objects.filter(
                    team1=player.team, status__in=["live", "played"]).count()
                + Match.objects.filter(team2=player.team,
                                       status__in=["live", "played"]).count()
            )
            if player.position == "GK":
                player.clean_sheets = (
                    Match.objects.filter(
                        team1=player.team, status__in=["live", "played"], team2_goals=0
                    ).count()
                    + Match.objects.filter(
                        team2=player.team, status__in=["live", "played"], team1_goals=0
                    ).count()
                )
            player.save()

        for player in self.team2.players.all():
            player.games_played = (
                Match.objects.filter(
                    team1=player.team, status__in=["live", "played"]).count()
                + Match.objects.filter(team2=player.team,
                                       status__in=["live", "played"]).count()
            )
            player.mvps = Match.objects.filter(mvp=player).count()
            if player.position == "GK":
                player.clean_sheets = (
                    Match.objects.filter(
                        team1=player.team, status__in=["live", "played"], team2_goals=0
                    ).count()
                    + Match.objects.filter(
                        team2=player.team, status__in=["live", "played"], team1_goals=0
                    ).count()
                )
            player.save()

    @staticmethod
    def team_update(team):
        team.wins = 0
        team.losses = 0
        team.draws = 0
        team.games_played = 0
        team.goals_scored = 0
        team.goals_conceded = 0

        for match in Match.objects.filter(team1=team, status__in=["live", "played"]):
            team.games_played += 1
            team.goals_scored += match.team1_goals
            team.goals_conceded += match.team2_goals
            if match.team1_goals > match.team2_goals:
                team.wins += 1
            elif match.team1_goals < match.team2_goals:
                team.losses += 1
            else:
                team.draws += 1

        for match in Match.objects.filter(team2=team, status__in=["live", "played"]):
            team.games_played += 1
            team.goals_scored += match.team2_goals
            team.goals_conceded += match.team1_goals
            if match.team2_goals > match.team1_goals:
                team.wins += 1
            elif match.team2_goals < match.team1_goals:
                team.losses += 1
            else:
                team.draws += 1

        team.goal_difference = team.goals_scored - team.goals_conceded
        team.points = team.wins * 3 + team.draws
        team.save()

    def save(self, *args, **kwargs):
        if self.status == "declined":
            self.delete()
        else:
            super().save(*args, **kwargs)
            self.update_players()
            for team in Team.objects.all():
                self.team_update(team)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_players()
        for team in Team.objects.all():
            self.team_update(team)

    class Meta:
        ordering = ("date", "time")
        verbose_name_plural = "matches"

    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.date} at {self.time}"


class MatchPlayerStats(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    goals_scored = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    yellow_cards = models.PositiveIntegerField(default=0)
    red_cards = models.PositiveIntegerField(default=0)

    def __str__(self, *args, **kwargs):
        return f"Stats"

    class Meta:
        verbose_name_plural = "match player stats"
