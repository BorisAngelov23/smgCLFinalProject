from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory

from smgCLFinalProject.team.models import Team, Player


class TeamRegistrationForm(forms.ModelForm):
    paralelki = forms.MultipleChoiceField(
        choices=[('A', 'A'), ('B', 'B'), ('V', 'V'), ('G', 'G'), ('D', 'D'), ('E', 'E')],
        widget=forms.CheckboxSelectMultiple)
    captain_player_created = False

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TeamRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['paralelki'].label = ''

    def clean(self):
        cleaned_data = super().clean()
        paralelki = cleaned_data.get('paralelki')
        if len(paralelki) > 3 and self.user.grade == '9':
            raise ValidationError("You can't choose more than 3 classes")
        if len(paralelki) > 2 and self.user.grade == '10':
            raise ValidationError("You can't choose more than 2 classes")
        if len(paralelki) > 1 and (self.user.grade == '11' or self.user.grade == '12'):
            raise ValidationError("You can't choose more than 1 class")
        if len(paralelki) < 6 and self.user.grade == '8':
            raise ValidationError("You must choose all 6 classes")
        return cleaned_data

    def save(self, commit=True):
        team = super().save(commit=False)
        self.clean()
        captain = self.instance.captain
        captain_player = Player(first_name=captain.first_name, last_name=captain.last_name, grade=captain.grade,
                                paralelka=captain.paralelka, team=team, is_captain=True, position=captain.position, )
        team.grade = captain.grade
        team.name = f"{team.grade}{''.join(team.paralelki)}"
        if captain_player.grade == 12 or captain_player.grade == 11:
            team.paralelki = [captain_player.paralelka]
        elif captain_player.grade == 8:
            team.paralelki = ['A', 'B', 'V', 'G', 'D', 'E']
            team.name = f"8sboren"
        if commit:
            team.save()
            if not self.captain_player_created:
                captain_player.save()
                self.captain_player_created = True
        return team

    class Meta:
        model = Team
        fields = ('paralelki',)


class PlayerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = ''
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['first_name'].required = True
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
        self.fields['last_name'].required = True
        self.fields['grade'].label = ''
        self.fields['grade'].required = True
        self.fields['paralelka'].label = ''
        self.fields['paralelka'].required = True
        self.fields['position'].label = ''
        self.fields['position'].required = True

    class Meta:
        title = 'Player'
        model = Player
        fields = ('first_name', 'last_name', 'grade', 'paralelka', 'position', 'picture')


#
# # TODO add validation for transfers, paralelki, players grades, paginate make errors look nice, manually added captain validate not to be in players, one GK required, save input when error
#
#
# class TeamRegistrationForm(forms.ModelForm):
#     players = PlayerCreationFormSet()
#     paralelki = forms.MultipleChoiceField(choices=[('A', 'A'), ('B', 'B'), ('V', 'V'), ('G', 'G'), ('D', 'D'), ('E', 'E')], widget=forms.CheckboxSelectMultiple)
#     captain_player_created = False
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(TeamRegistrationForm, self).__init__(*args, **kwargs)
#         self.fields['paralelki'].label = 'Classes'
#         if user.grade == '12' or user.grade == '11':
#             self.fields['paralelki'].required = False
#             self.fields['paralelki'].widget = forms.HiddenInput()
#             self.fields.pop('paralelki')
#         for i, form in enumerate(self.players.forms):
#             if i < 5:
#                 form.fields['first_name'].required = True
#                 form.fields['last_name'].required = True
#                 form.fields['grade'].required = True
#                 form.fields['position'].required = True
#             else:
#                 form.fields['first_name'].required = False
#                 form.fields['last_name'].required = False
#                 form.fields['grade'].required = False
#                 form.fields['position'].required = False
#
#     def clean(self):
#         cleaned_data = super().clean()
#         positions = []
#         for player_form in self.players:
#             player = player_form.save(commit=False)
#             positions.append(player.position)
#         if 'GK' not in positions:
#             raise ValidationError('You must have at least one goalkeeper.')
#         return cleaned_data
#
#     def save(self, commit=True):
#         team = super().save(commit=False)
#         captain = self.instance.captain
#         captain_player = Player(first_name=captain.first_name, last_name=captain.last_name, grade=captain.grade,
#                                 paralelka=captain.paralelka, team=team, is_captain=True)
#         team.grade = captain.grade
#         team.name = f"{team.grade}{''.join(team.paralelki)}"
#         if captain_player.grade == 12 or captain_player.grade == 11:
#             team.paralelki = [captain_player.paralelka]
#         elif captain_player.grade == 8:
#             team.paralelki = ['A', 'B', 'V', 'G', 'D', 'E']
#         if commit:
#             team.save()
#             if not self.captain_player_created:
#                 captain_player.save()
#                 self.captain_player_created = True
#             for player_form in self.players:
#                 player = player_form.save(commit=False)
#                 player.team = team
#                 player.is_captain = False
#                 player.save()
#         return team
#
#     class Meta:
#         model = Team
#         fields = ('paralelki',)
