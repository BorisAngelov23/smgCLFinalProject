# matches/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView

from .forms import ArrangeMatchForm, MatchResponseForm
from .models import Match


class MatchRequestSent(TemplateView):
    template_name = 'match/match_request_sent.html'


class ArrangeMatch(CreateView):
    form_class = ArrangeMatchForm
    template_name = 'match/arrange_match.html'
    success_url = reverse_lazy('match_request_sent')

    def form_valid(self, form):
        match = form.save(commit=False)
        match.team1 = self.request.user.team
        match.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MatchResponse(UpdateView):
    form_class = MatchResponseForm
    template_name = 'match/respond_to_match.html'
    # TODO change success_url to matches page
    success_url = reverse_lazy('homepage')

    def get_queryset(self):
        return Match.objects.filter(team2=self.request.user.team, status='pending')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['match'] = Match.objects.filter(team2=self.request.user.team, status='pending').first()
        return context
