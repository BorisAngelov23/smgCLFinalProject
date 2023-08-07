from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from smgCLFinalProject.team.forms import TeamRegistrationForm, PlayerForm


class TeamRegister(CreateView, LoginRequiredMixin):
    form_class = TeamRegistrationForm
    template_name = 'team/choose_classes.html'
    success_url = reverse_lazy('add_players')

    def get(self, request, *args, **kwargs):
        try:
            if request.user.team:
                return redirect('homepage')
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
        kwargs['user'] = self.request.user
        return kwargs


def create_multiple_players(request):
    FootballPlayerFormSet = formset_factory(PlayerForm, extra=9)
    if request.method == 'GET':
        formset = FootballPlayerFormSet()
        return render(request, 'team/add_players.html', {'formset': formset})
    else:
        formset = FootballPlayerFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                player = form.save(commit=False)
                player.team = request.user.team
                form.save()
            return redirect('homepage')
        else:
            return render(request, 'team/add_players.html', {'formset': formset})
