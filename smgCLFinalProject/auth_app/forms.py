from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from smgCLFinalProject.auth_app.models import CaptainUser


class CaptainRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=12, required=False)
    facebook_link = forms.URLField()
    grade = forms.Select(choices=[('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')])
    paralelka = forms.Select(choices=[('A', 'A'), ('B', 'B'), ('V', 'V'), ('G', 'G'), ('D', 'D'), ('E', 'E')])
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].label = ''
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['first_name'].label = ''
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
        self.fields['phone_number'].label = ''
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Phone Number'})
        self.fields['facebook_link'].label = ''
        self.fields['facebook_link'].widget.attrs.update(
            {'placeholder': 'Facebook Link', 'title': 'Enter your Facebook page link for the Messenger group'})
        self.fields['grade'].label = ''
        self.fields['paralelka'].label = ''
        self.fields['position'].label = ''

    def clean(self):
        cleaned_data = super().clean()
        grade = cleaned_data.get('grade')
        registered_captains_count_from_the_same_grade = CaptainUser.objects.filter(grade=grade).count()
        if grade == '8' and registered_captains_count_from_the_same_grade > 0:
            raise forms.ValidationError('There is already a captain from 8th grade')
        elif grade == '9' and registered_captains_count_from_the_same_grade > 1:
            raise forms.ValidationError('There are already 2 captains from 9th grade')
        elif grade == '10' and registered_captains_count_from_the_same_grade > 2:
            raise forms.ValidationError('There are already 3 captains from 10th grade')
        elif grade == '11' and registered_captains_count_from_the_same_grade > 5:
            raise forms.ValidationError('There are already 6 captains from 11th grade')
        elif grade == '12' and registered_captains_count_from_the_same_grade > 5:
            raise forms.ValidationError('There are already 6 captains from 12th grade')


    def save(self, commit=True):
        user = super().save(commit=False)
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        grade = self.cleaned_data['grade']
        paralelka = self.cleaned_data['paralelka']
        user.username = f'{first_name}{last_name}{grade}{paralelka}'
        if commit:
            user.save()
        return user

    class Meta:
        model = CaptainUser
        fields = ('first_name', 'last_name', 'grade', 'paralelka', 'password1', 'password2', 'email', 'facebook_link',
                  'phone_number', 'position')


class CaptainEditForm(UserChangeForm):
    password = None

    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CaptainUser
        fields = (
            'first_name', 'last_name', 'grade', 'paralelka', 'email', 'facebook_link', 'phone_number',
            'profile_picture', 'position')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['first_name'].label = ''
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
        self.fields['phone_number'].label = ''
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Phone Number'})
        self.fields['facebook_link'].label = ''
        self.fields['facebook_link'].widget.attrs.update(
            {'placeholder': 'Facebook Link', 'title': 'Enter your Facebook page link for the Messenger group'})
        self.fields['grade'].label = ''
        self.fields['paralelka'].label = ''
        self.fields['profile_picture'].label = ''

    def save(self, commit=True):
        user = super().save(commit=False)
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        grade = self.cleaned_data['grade']
        paralelka = self.cleaned_data['paralelka']
        user.username = f'{first_name}{last_name}{grade}{paralelka}'
        if commit:
            user.save()
        return user
