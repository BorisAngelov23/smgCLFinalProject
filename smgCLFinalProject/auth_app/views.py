from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from smgCLFinalProject.auth_app.forms import CaptainRegistrationForm


class CaptainRegister(CreateView):
    form_class = CaptainRegistrationForm
    template_name = 'auth_app/register.html'
    success_url = reverse_lazy('homepage')  # TODO: Change this to the register team page
