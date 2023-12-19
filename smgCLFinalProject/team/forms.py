from django import forms
from django.core.exceptions import ValidationError

from smgCLFinalProject.team.models import Team, Player


class TeamRegistrationForm(forms.ModelForm):
    paralelki = forms.MultipleChoiceField(
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("V", "V"),
            ("G", "G"),
            ("D", "D"),
            ("E", "E"),
        ],
        widget=forms.CheckboxSelectMultiple,
    )
    captain_player_created = False

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(TeamRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["paralelki"].label = ""

    def clean(self):
        cleaned_data = super().clean()
        paralelki = cleaned_data.get("paralelki")
        if len(paralelki) < 1:
            raise ValidationError("You must choose at least 1 class")
        if len(paralelki) > 3 and self.user.grade == "9":
            raise ValidationError("You can't choose more than 3 classes")
        if len(paralelki) > 1 and (self.user.grade == "11" or self.user.grade == "12" or self.user.grade == "10"):
            raise ValidationError("You can't choose more than 1 class")
        if len(paralelki) < 6 and self.user.grade == "8":
            raise ValidationError("You must choose all 6 classes")
        if self.user.paralelka not in paralelki:
            raise ValidationError("You must choose your class")
        return cleaned_data

    def save(self, commit=True):
        team = super().save(commit=False)
        self.clean()
        captain = self.instance.captain
        team.grade = captain.grade
        if captain.grade == '8':
            team.paralelki = ["A", "B", "V", "G", "D", "E"]
            team.name = f"8sboren"
        else:
            team.name = f"{team.grade}{''.join(team.paralelki)}"

        captain_player = Player(
            first_name=captain.first_name,
            last_name=captain.last_name,
            grade=captain.grade,
            paralelka=captain.paralelka,
            team=team,
            is_captain=True,
            position=captain.position,
            picture=captain.profile_picture,
        )

        if commit:
            team.save()
            if not self.captain_player_created:
                captain_player.save()
                self.captain_player_created = True
        return team

    class Meta:
        model = Team
        fields = ("paralelki",)


class PlayerForm(forms.ModelForm):
    picture = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["first_name"].label = ""
        self.fields["first_name"].widget.attrs.update(
            {"placeholder": "First Name"})
        self.fields["first_name"].required = True
        self.fields["last_name"].label = ""
        self.fields["last_name"].widget.attrs.update(
            {"placeholder": "Last Name"})
        self.fields["last_name"].required = True
        self.fields["grade"].label = ""
        self.fields["grade"].required = True
        self.fields["paralelka"].label = ""
        self.fields["paralelka"].required = True
        self.fields["position"].label = ""
        self.fields["position"].required = True

    def clean(self):
        cleaned_data = super().clean()
        fn = cleaned_data.get("first_name")
        ln = cleaned_data.get("last_name")
        paralelka = cleaned_data.get("paralelka")
        grade = cleaned_data.get("grade")
        pos = cleaned_data.get("position")
        picture = cleaned_data.get("picture")
        if (
            fn is not None
            and ln is not None
            and paralelka is not None
            and grade is not None
            and pos is not None
        ):
            if not fn[0].isupper() or not ln[0].isupper():
                raise forms.ValidationError(
                    "Your name must start with a capital letter")
            if not fn.isalpha() or not ln.isalpha():
                raise forms.ValidationError(
                    "Name should only contain letters.")
            if len(fn) < 2 or len(ln) < 2 or len(fn) > 30 or len(ln) > 30:
                raise forms.ValidationError(
                    "Name should be at least 2 letters long and max 30 letters long."
                )
            if fn == self.user.first_name and ln == self.user.last_name:
                raise forms.ValidationError(
                    "You can not add yourself as a player.")
            players = Player.objects.filter(team=self.user.team)
            if (
                    grade != self.user.grade
                    or paralelka not in self.user.team.paralelki
            ):
                if self.user.team.grade == '8' or self.user.team.grade == '9':
                    raise forms.ValidationError(
                        "No transfers allowed for teams from 8th, 9th and 10th grade."
                    )
            if self.user.grade == '11' or self.user.grade == '12' or self.user.grade == '10':
                transfer = False
                for player in players:
                    if (
                            player.grade != self.user.grade
                            or player.paralelka not in self.user.team.paralelki
                    ):
                        if transfer:
                            raise forms.ValidationError(
                                "Up to 1 transfer for teams from 10th and 12th."
                            )
                        transfer = True
        return cleaned_data

    class Meta:
        title = "Player"
        model = Player
        fields = (
            "first_name",
            "last_name",
            "grade",
            "paralelka",
            "position",
            "picture",
        )


class PlayerEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["first_name"].label = ""
        self.fields["first_name"].widget.attrs.update(
            {"placeholder": "First Name"})
        self.fields["first_name"].required = True
        self.fields["first_name"].disabled = True
        self.fields["last_name"].label = ""
        self.fields["last_name"].widget.attrs.update(
            {"placeholder": "Last Name"})
        self.fields["last_name"].required = True
        self.fields["last_name"].disabled = True
        self.fields["grade"].label = ""
        self.fields["grade"].required = True
        self.fields["grade"].disabled = True
        self.fields["paralelka"].label = ""
        self.fields["paralelka"].required = True
        self.fields["paralelka"].disabled = True
        self.fields["position"].label = ""
        self.fields["position"].required = True

    def clean(self):
        players = Player.objects.filter(team=self.user.team)
        cleaned_data = super().clean()
        transfer = False
        for player in players:
            if (
                player.grade != self.user.grade
                or player.paralelka not in self.user.team.paralelki
            ):
                if transfer or player.team.grade == '8' or player.team.grade == '9':
                    raise forms.ValidationError(
                        "Up to 1 transfer for teams from 10th to 12th grade and 0 for teams from 8th and 9th grade."
                    )
                transfer = True
        return cleaned_data

    class Meta:
        title = "Player"
        model = Player
        fields = (
            "first_name",
            "last_name",
            "grade",
            "paralelka",
            "position",
            "picture",
        )
