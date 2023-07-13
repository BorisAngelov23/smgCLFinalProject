from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView

from smgCLFinalProject.auth_app.forms import CaptainRegistrationForm, CaptainEditForm
from smgCLFinalProject.auth_app.models import CaptainUser


class CaptainRegister(CreateView):
    form_class = CaptainRegistrationForm
    template_name = 'auth_app/register.html'
    success_url = reverse_lazy('team_register')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class CaptainLogin(LoginView):
    template_name = 'auth_app/login.html'
    form_class = AuthenticationForm


class CaptainLogout(LogoutView):
    pass


class CaptainDetails(DetailView):
    template_name = 'auth_app/captain_details.html'
    model = CaptainUser


class CaptainEdit(UpdateView):
    model = CaptainUser
    form_class = CaptainEditForm
    template_name = 'auth_app/captain_edit.html'
    success_url = reverse_lazy('homepage')
