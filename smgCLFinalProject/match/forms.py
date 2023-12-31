from datetime import time, date

from django import forms
from django.utils import timezone

from .models import Match


class ArrangeMatchForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["team2"].label = "Opponent"

    def clean(self):
        cleaned_data = super().clean()
        match_date = cleaned_data.get("date")
        match_time = cleaned_data.get("time")
        team2 = cleaned_data.get("team2")

        if Match.objects.filter(team1=self.user.team).count() + Match.objects.filter(team2=self.user.team).count() >= 6:
            raise forms.ValidationError(
                "You cannot arrange more than 6 matches overall."
            )

        if team2 == self.user.team:
            raise forms.ValidationError(
                "You cannot arrange a match with yourself.")
        if (
                Match.objects.filter(
                   team1=team2, team2=self.user.team, date=match_date
                ).exists()
                or Match.objects.filter(
            team1=self.user.team, team2=team2, date=match_date
        ).exists()
        ):
            raise forms.ValidationError(
                "You already have a match with this team on this day."
            )
        if Match.objects.filter(date=match_date, time=match_time, team2=team2).exists():
            raise forms.ValidationError(
                "You already have a match at that date and time with that opponent."
            )
        if Match.objects.filter(date=match_date, time=match_time).exists():
            raise forms.ValidationError(
                "There is already a match at that date and time."
            )
        if match_date < timezone.now().date() or (
                match_date == timezone.now().date() and match_time < timezone.now().time()):
            raise forms.ValidationError(
                "You cannot arrange a match in the past.")
        if match_time < time(7, 30) or match_time > time(19, 10):
            raise forms.ValidationError(
                "You cannot arrange a match before 7:30 or after 19:10."
            )
        if match_date < date(2024, 1, 1):
            raise forms.ValidationError(
                "You cannot arrange a match before the start of the season."
            )
        if team2 not in self.user.team.allowed_teams.all():
            raise forms.ValidationError(
                "You cannot arrange a match with this team."
            )

    class Meta:
        model = Match
        fields = ("date", "time", "team2")

        widgets = {
            'date': forms.DateInput(attrs={'required': True}),
            'time': forms.TimeInput(attrs={'required': True}),
        }


class MatchResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].label = "Response"
        self.fields["status"].choices = [
            ("accepted", "Accept"),
            ("declined", "Decline"),
        ]

    class Meta:
        model = Match
        fields = ("status",)


class MatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            team1_players = self.instance.team1.players.all()
            team2_players = self.instance.team2.players.all()
            valid_players = team1_players | team2_players
            self.fields['mvp'].queryset = valid_players
