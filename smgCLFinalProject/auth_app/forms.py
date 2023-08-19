from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from smgCLFinalProject.auth_app.models import CaptainUser
from smgCLFinalProject.team.models import Player, Team


class CaptainRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=12, required=False)
    facebook_link = forms.URLField()
    grade = forms.Select(
        choices=[("8", "8"), ("9", "9"), ("10", "10"),
                 ("11", "11"), ("12", "12")]
    )
    paralelka = forms.Select(
        choices=[("A", "A"), ("B", "B"), ("V", "V"),
                 ("G", "G"), ("D", "D"), ("E", "E")]
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = ""
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Password"})
        self.fields["password2"].label = ""
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirm Password"}
        )
        self.fields["email"].label = ""
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["first_name"].label = ""
        self.fields["first_name"].widget.attrs.update(
            {"placeholder": "First Name"})
        self.fields["last_name"].label = ""
        self.fields["last_name"].widget.attrs.update(
            {"placeholder": "Last Name"})
        self.fields["phone_number"].label = ""
        self.fields["phone_number"].widget.attrs.update(
            {"placeholder": "Phone Number"})
        self.fields["facebook_link"].label = ""
        self.fields["facebook_link"].widget.attrs.update(
            {
                "placeholder": "Facebook Link",
                "title": "Enter your Facebook page link for the Messenger group",
            }
        )
        self.fields["grade"].label = ""
        self.fields["paralelka"].label = ""
        self.fields["position"].label = ""

    def clean(self):
        cleaned_data = super().clean()
        grade = cleaned_data.get("grade")
        paralelka = cleaned_data.get("paralelka")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if CaptainUser.objects.filter(
            first_name=first_name, last_name=last_name, grade=grade, paralelka=paralelka
        ).exists():
            raise forms.ValidationError(
                "You are already registered as a captain")

        if CaptainUser.objects.filter(
            email=cleaned_data.get("email")
        ).exists():
            raise forms.ValidationError(
                "This email is already registered")

        if CaptainUser.objects.filter(
            facebook_link=cleaned_data.get("facebook_link")
        ).exists():
            raise forms.ValidationError(
                "This Facebook link is already registered")

        if not first_name[0].isupper() or not last_name[0].isupper():
            raise forms.ValidationError(
                "Your name must start with a capital letter")

        if not first_name.isalpha() or not last_name.isalpha():
            raise forms.ValidationError("Your name must contain only letters")

        registered_captains_count_from_the_same_grade = CaptainUser.objects.filter(
            grade=grade
        ).count()

        if grade == "8" and registered_captains_count_from_the_same_grade > 0:
            raise forms.ValidationError(
                "There is already a captain from 8th grade")

        elif grade == "9" and registered_captains_count_from_the_same_grade > 1:
            raise forms.ValidationError(
                "There are already 2 captains from 9th grade")

        elif grade == "10" and registered_captains_count_from_the_same_grade > 2:
            raise forms.ValidationError(
                "There are already 3 captains from 10th grade")

        elif grade == "11" and registered_captains_count_from_the_same_grade > 5:
            raise forms.ValidationError(
                "There are already 6 captains from 11th grade")

        elif grade == "12" and registered_captains_count_from_the_same_grade > 5:
            raise forms.ValidationError(
                "There are already 6 captains from 12th grade")

        if Team.objects.filter(grade=grade, paralelki__contains=[paralelka]).exists():
            raise forms.ValidationError("Your class already has a team.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        grade = self.cleaned_data["grade"]
        paralelka = self.cleaned_data["paralelka"]
        user.username = f"{first_name}{last_name}{grade}{paralelka}"
        if commit:
            user.save()
        return user

    class Meta:
        model = CaptainUser
        fields = (
            "first_name",
            "last_name",
            "grade",
            "paralelka",
            "password1",
            "password2",
            "email",
            "facebook_link",
            "phone_number",
            "position",
        )


class CaptainEditForm(UserChangeForm):
    password = None

    profile_picture = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = CaptainUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "facebook_link",
            "phone_number",
            "profile_picture",
            "position",
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["email"].label = ""
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["first_name"].label = ""
        self.fields["first_name"].required = True
        self.fields["first_name"].disabled = True
        self.fields["first_name"].widget.attrs.update(
            {"placeholder": "First Name"})
        self.fields["last_name"].label = ""
        self.fields["last_name"].widget.attrs.update(
            {"placeholder": "Last Name"})
        self.fields["last_name"].required = True
        self.fields["last_name"].disabled = True
        self.fields["phone_number"].label = ""
        self.fields["phone_number"].widget.attrs.update(
            {"placeholder": "Phone Number"})
        self.fields["phone_number"].required = False
        self.fields["facebook_link"].label = ""
        self.fields["facebook_link"].required = True
        self.fields["facebook_link"].widget.attrs.update(
            {
                "placeholder": "Facebook Link",
                "title": "Enter your Facebook page link for the Messenger group",
            }
        )
        self.fields["profile_picture"].label = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        user.username = f"{first_name}{last_name}{self.user.grade}{self.user.paralelka}"
        player = Player.objects.get(
            first_name=first_name, last_name=last_name, is_captain=True
        )
        player.position = self.cleaned_data["position"]
        player.picture = self.cleaned_data["profile_picture"]
        player.save()
        if commit:
            user.save()
        return user
