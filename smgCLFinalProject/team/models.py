from django.contrib.postgres.fields import ArrayField
from django.db import models

from smgCLFinalProject.auth_app.models import CaptainUser


class Player(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    grade = models.CharField(
        max_length=2,
        choices=[
            ("", "Grade"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
        ],
    )
    paralelka = models.CharField(
        max_length=1,
        choices=[
            ("", "Class"),
            ("A", "A"),
            ("B", "B"),
            ("V", "V"),
            ("G", "G"),
            ("D", "D"),
            ("E", "E"),
        ],
    )
    picture = models.ImageField(
        upload_to="player_pictures", null=True, blank=True)
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="players")
    is_captain = models.BooleanField(default=False)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)
    position = models.CharField(
        max_length=2,
        choices=[
            ("", "Position"),
            ("GK", "Goalkeeper"),
            ("DF", "Defender"),
            ("MF", "Midfielder"),
            ("FW", "Forward"),
        ],
        default="",
        null=False,
        blank=False,
    )
    mvps = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.team.name}"

    class Meta:
        ordering = ("grade", "paralelka", "first_name", "last_name")


class Team(models.Model):
    captain = models.OneToOneField(
        CaptainUser, on_delete=models.CASCADE, related_name="team", default=None
    )
    name = models.CharField(max_length=8, unique=True, default=None)
    grade = models.CharField(
        max_length=2,
        choices=[
            ("", "Grade"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
        ],
        default=None,
    )
    paralelki = ArrayField(
        base_field=models.CharField(max_length=1),
        size=6,
        default=list,
        blank=True,
        null=True,
    )
    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    # add allowed teams to play against which are given by the admins
    allowed_teams = models.ManyToManyField("Team", related_name="allowed_teams_vs")

    def __str__(self):
        return self.name
