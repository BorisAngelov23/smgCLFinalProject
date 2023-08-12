from datetime import time, date

from django import forms
from django.utils import timezone

from .models import Match


class ArrangeMatchForm(forms.ModelForm):
    # date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    # time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'timepicker'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['team2'].label = 'Opponent'

    def clean(self):
        cleaned_data = super().clean()
        match_date = cleaned_data.get('date')
        match_time = cleaned_data.get('time')
        team2 = cleaned_data.get('team2')

        if team2 == self.user.team:
            raise forms.ValidationError(
                "You cannot arrange a match with yourself."
            )
        if Match.objects.filter(team1=team2, team2=self.user.team, date=match_date).exists() or Match.objects.filter(
                team1=self.user.team, team2=team2, date=match_date).exists():
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
        if match_date < timezone.now().date():
            raise forms.ValidationError(
                "You cannot arrange a match in the past."
            )
        if match_date == timezone.now().date() and match_time < timezone.now().time():
            raise forms.ValidationError(
                "You cannot arrange a match in the past."
            )
        if match_time < time(7, 30) or match_time > time(19, 10):
            raise forms.ValidationError(
                "You cannot arrange a match before 7:30 or after 19:10."
            )
        if match_date < date(2023, 9, 15):
            raise forms.ValidationError(
                "You cannot arrange a match before the start of the season."
            )

    class Meta:
        model = Match
        fields = ('date', 'time', 'team2')


class MatchResponseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].label = 'Response'
        self.fields['status'].choices = [('accepted', 'Accept'), ('declined', 'Decline')]

    class Meta:
        model = Match
        fields = ('status',)