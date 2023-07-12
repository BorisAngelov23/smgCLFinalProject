from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CaptainRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=12, required=False)
    facebook_link = forms.URLField()
    grade = forms.CharField(max_length=2)
    paralelka = forms.MultipleChoiceField(
        choices=[('A', 'A'), ('B', 'B'), ('V', 'V'), ('G', 'G'), ('D', 'D'), ('E', 'E')])

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name',
                  'phone_number', 'facebook_link', 'grade', 'paralelka')
