import os

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView

from smgCLFinalProject.auth_app.forms import CaptainRegistrationForm, CaptainEditForm
from smgCLFinalProject.auth_app.models import CaptainUser


class CaptainRegister(CreateView):
    form_class = CaptainRegistrationForm
    template_name = "auth_app/register.html"
    success_url = reverse_lazy("choose_classes")

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)

        self.send_welcome_email(self, self.object.email)

        return result

    @staticmethod
    def send_welcome_email(self, user_email):
        subject = "Welcome to the SMG Champions League!"
        message = ("Thank you for registering to our website. Enjoy the beautiful game and good luck!"
                   "\nSMG Champions League Team")
        from_email = os.environ.get("EMAIL_HOST_USER")
        recipient_list = [user_email]

        # Use fail_silently=False for development; set it to True in production #TODO
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)


class CaptainLogin(LoginView):
    template_name = "auth_app/login.html"
    form_class = AuthenticationForm


class CaptainLogout(LogoutView):
    pass


class CaptainDetails(DetailView):
    template_name = "auth_app/captain_details.html"
    model = CaptainUser

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.request.user.pk)


class CaptainEdit(UpdateView):
    model = CaptainUser
    form_class = CaptainEditForm
    template_name = "auth_app/captain_edit.html"

    def get_success_url(self):
        return reverse_lazy("captain_details", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(CaptainEdit, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
