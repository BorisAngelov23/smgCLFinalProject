from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from rest_framework.views import APIView

from .forms import ArrangeMatchForm, MatchResponseForm
from .models import Match

from rest_framework.generics import ListAPIView
from .models import MatchPlayerStats
from rest_framework import serializers


class MatchRequestSent(TemplateView, LoginRequiredMixin):
    template_name = 'match/match_request_sent.html'


class ArrangeMatch(CreateView, LoginRequiredMixin):
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


class MatchResponse(UpdateView, LoginRequiredMixin):
    form_class = MatchResponseForm
    template_name = 'match/respond_to_match.html'
    success_url = reverse_lazy('matches')

    def get_queryset(self):
        return Match.objects.filter(team2=self.request.user.team, status='pending')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['match'] = Match.objects.filter(team2=self.request.user.team, status='pending').first()
        return context


class MatchPlayerStatsSerializer(serializers.ModelSerializer):
    player_name = serializers.SerializerMethodField()
    player_id = serializers.SerializerMethodField()

    class Meta:
        model = MatchPlayerStats
        fields = ['player_name', 'goals_scored', 'player_id']

    def get_player_name(self, obj):
        return str(obj.player)

    def get_player_id(self, obj):
        return obj.player.id


class MatchGoalscorersView(APIView):
    def get(self, request, match_id, *args, **kwargs):
        match_stats = MatchPlayerStats.objects.filter(match_id=match_id)
        serializer = MatchPlayerStatsSerializer(match_stats, many=True)
        return JsonResponse(serializer.data, safe=False)


class MatchesTemplateView(TemplateView):
    template_name = 'match/matches.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['matches'] = Match.objects.all()
        return context
