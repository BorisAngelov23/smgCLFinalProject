from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, BaseFormSet
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, TemplateView

from smgCLFinalProject.match.models import Match
from smgCLFinalProject.team.forms import (
    TeamRegistrationForm,
    PlayerForm,
    PlayerEditForm,
)
from smgCLFinalProject.team.models import Player, Team


class TeamRegister(CreateView, LoginRequiredMixin):
    form_class = TeamRegistrationForm
    template_name = "team/choose_classes.html"
    success_url = reverse_lazy("add_players")

    def get(self, request, *args, **kwargs):
        try:
            if request.user.team:
                return redirect("homepage")
        except AttributeError:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.captain = self.request.user
        if form.is_valid():
            form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super(TeamRegister, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class FirstFiveRequiredFormset(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(FirstFiveRequiredFormset, self).__init__(*args, **kwargs)
        self.user = kwargs.pop("user", None)
        i = 1
        for form in self.forms:
            if i < 2:
                form.empty_permitted = False
            i += 1

    def clean(self):
        user = getattr(self, "user", None)
        gk = False
        transfers = 0
        for form in self.forms:
            if form.cleaned_data.get("position") == "GK":
                gk = True
            if form.has_changed():
                if (
                        form.cleaned_data.get("paralelka") not in user.team.paralelki
                        or form.cleaned_data.get("grade") != user.grade
                ):
                    transfers += 1
        if not gk and Player.objects.filter(team=user.team, position="GK").count() < 1:
            raise forms.ValidationError(
                "You must have at least one goalkeeper")
        if transfers > 1:
            raise forms.ValidationError(
                "You can have up to 1 transfer (must be from your grade) in your team."
            )
        if transfers == 1 and (user.team.grade == "8" or user.team.grade == "9"):
            raise forms.ValidationError(
                "You can't have transfers in your team if you are from 8th, 9th or 10th grade."
            )


@login_required
def players_add(request):
    FootballPlayerFormSet = formset_factory(
        PlayerForm, extra=9, formset=FirstFiveRequiredFormset
    )
    if request.method == "GET":
        if request.user.added_players:
            return redirect("homepage")
        formset = FootballPlayerFormSet()
        return render(request, "team/add_players.html", {"formset": formset})
    else:
        formset = FootballPlayerFormSet(
            request.POST, request.FILES, form_kwargs={"user": request.user}
        )
        formset.user = request.user
        if formset.is_valid():
            for form in formset:
                if form.is_valid:
                    form.clean()
                    if form.has_changed():
                        player = form.save(commit=False)
                        player.team = request.user.team
                        form.save()
            request.user.added_players = True
            request.user.save()
            return redirect("homepage")
        else:
            return render(request, "team/add_players.html", {"formset": formset})


@login_required
def player_add(request):
    FootballPlayerFormSet = formset_factory(
        PlayerForm, extra=1, formset=FirstFiveRequiredFormset
    )
    if request.method == "GET":
        if Player.objects.filter(team=request.user.team).count() >= 12:
            return redirect("homepage")
        formset = FootballPlayerFormSet()
        return render(request, "team/add_extra_players.html", {"formset": formset})
    else:
        formset = FootballPlayerFormSet(
            request.POST, request.FILES, form_kwargs={"user": request.user}
        )
        formset.user = request.user
        if formset.is_valid():
            for form in formset:
                if form.is_valid:
                    form.clean()
                    formset.clean()
                    if form.has_changed():
                        player = form.save(commit=False)
                        player.team = request.user.team
                        form.save()
            request.user.added_players = True
            request.user.save()
            return redirect("homepage")
        else:
            return render(request, "team/add_extra_players.html", {"formset": formset})


@login_required
def players_edit(request):
    FootballPlayerFormSet = formset_factory(
        PlayerEditForm, extra=0, formset=FirstFiveRequiredFormset
    )
    players = Player.objects.filter(
        team=request.user.team).exclude(is_captain=True)
    initial_data = [
        {
            "player_id": player.id,
            "first_name": player.first_name,
            "last_name": player.last_name,
            "grade": player.grade,
            "paralelka": player.paralelka,
            "position": player.position,
            # "picture": player.picture,
        }
        for player in players
    ]
    players_to_update = []
    if request.method == "POST":
        formset = FootballPlayerFormSet(
            request.POST,
            request.FILES,
            form_kwargs={"user": request.user},
            initial=initial_data,
        )
        formset.user = request.user
        if formset.is_valid():
            for form in formset:
                if form.is_valid:
                    form.clean()
                    formset.clean()
                    if form.has_changed():
                        player = Player.objects.get(
                            first_name=form.cleaned_data.get("first_name"),
                            last_name=form.cleaned_data.get("last_name"),
                            team=request.user.team,
                        )
                        player.position = form.cleaned_data.get("position")
                        player.picture = form.cleaned_data.get("picture")
                        player.save()
                        players_to_update.append(player)
            Player.objects.bulk_update(
                players_to_update, fields=["position", "picture"]
            )
            return redirect("homepage")
    else:
        formset = FootballPlayerFormSet(initial=initial_data)

    return render(request, "team/edit_players.html", {"formset": formset})


def has_live_match(team):
    for match in Match.objects.filter(team1=team, status="live"):
        if match.team1_goals > match.team2_goals:
            return True, "win"
        elif match.team1_goals < match.team2_goals:
            return True, "loss"
        else:
            return True, "draw"
    for match in Match.objects.filter(team2=team, status="live"):
        if match.team1_goals > match.team2_goals:
            return True, "loss"
        elif match.team1_goals < match.team2_goals:
            return True, "win"
        else:
            return True, "draw"
    return False


class Standings(ListView):
    model = Team
    template_name = "team/standings.html"
    context_object_name = "teams"

    def get_queryset(self):
        teams = Team.objects.all().order_by(
            "-points", "-goal_difference", "-goals_scored", "name"
        )
        for team in teams:
            team.has_live_match = has_live_match(team)
        return teams


class PlayerStandings(ListView):
    model = Player
    template_name = "team/player_standings.html"
    context_object_name = "players"

    def get_queryset(self):
        return Player.objects.all().order_by(
            "-goals", "-assists", "first_name", "last_name"
        )


class PlayersFromTeam(ListView):
    model = Player
    template_name = "team/players_from_team.html"
    context_object_name = "players"

    def get_queryset(self):
        return Player.objects.filter(team=self.kwargs["pk"]).order_by(
            "-goals", "-assists", "first_name", "last_name"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = Team.objects.get(id=self.kwargs["pk"])
        context["upcoming_matches"] = Match.objects.filter(
            team1=self.kwargs["pk"], status="accepted"
        ) | Match.objects.filter(team2=self.kwargs["pk"], status="accepted")
        context["played_matches"] = Match.objects.filter(
            team1=self.kwargs["pk"], status="played"
        ) | Match.objects.filter(team2=self.kwargs["pk"], status="played")
        return context


class PlayerDetail(DetailView):
    model = Player
    template_name = "team/player_detail.html"
    context_object_name = "player"

    def get_context_data(self, **kwargs):
        POSITION_CHOICES = {
            "GK": "Goalkeeper",
            "DF": "Defender",
            "MF": "Midfielder",
            "FW": "Forward",
        }
        context = super().get_context_data(**kwargs)
        context["position"] = POSITION_CHOICES[self.object.position]
        player = Player.objects.get(id=self.kwargs["pk"])
        context["upcoming_matches"] = Match.objects.filter(
            team1=player.team, status="accepted"
        ) | Match.objects.filter(team2=player.team, status="accepted")
        context["played_matches"] = Match.objects.filter(
            team1=player.team, status="played"
        ) | Match.objects.filter(team2=player.team, status="played")
        return context


class TeamManagement(LoginRequiredMixin, ListView):
    template_name = "team/team_management.html"
    context_object_name = "players"

    def get_queryset(self):
        return Player.objects.filter(team=self.request.user.team).order_by(
            "-goals", "-assists", "first_name", "last_name"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = Team.objects.get(id=self.request.user.team.id)
        context["upcoming_matches"] = Match.objects.filter(
            team1=self.request.user.team, status="accepted"
        ) | Match.objects.filter(team2=self.request.user.team, status="accepted")
        context["played_matches"] = Match.objects.filter(
            team1=self.request.user.team, status="played"
        ) | Match.objects.filter(team2=self.request.user.team, status="played")
        return context
