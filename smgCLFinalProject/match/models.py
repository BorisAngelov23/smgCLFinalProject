from django.db import models

from smgCLFinalProject.auth_app.models import CaptainUser
from smgCLFinalProject.team.models import Team


class Match(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('played', 'Played')
    )

    RESPONSE_CHOICES = (
        ('accepted', 'Accept'),
        ('declined', 'Decline'),
    )

    date = models.DateField()
    time = models.TimeField()
    team1 = models.ForeignKey(Team, related_name='team1_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2_matches', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.date} at {self.time}"
