from django.shortcuts import render
from django.views.generic import CreateView, TemplateView


class TeamRegister(TemplateView):
    pass
    # form_class = TeamRegistrationForm #TODO: Create the form, the models (Player and Team), edit the template, change to CreateView
    template_name = 'team/register_team.html'
    # success_url = reverse_lazy('homepage')
