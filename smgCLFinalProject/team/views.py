from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, BaseFormSet
from django import forms
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


class FirstFiveRequiredFormset(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(FirstFiveRequiredFormset, self).__init__(*args, **kwargs)
        self.user = kwargs.pop('user', None)
        i = 1
        for form in self.forms:
            if i < 6:
                form.empty_permitted = False
            i += 1

    def clean(self):
        user = getattr(self, 'user', None)
        gk = False
        transfers = 0
        for form in self.forms:
            if form.cleaned_data.get("position") == "GK":
                gk = True

            if (form.cleaned_data.get("paralelka") not in user.team.paralelki or form.cleaned_data.get("grade") != user.grade) and not transfers:
                transfers += 1
        if not gk:
            raise forms.ValidationError("You must have at least one goalkeeper")
        if transfers > 1:
            raise forms.ValidationError("You can have up to 1 transfer (must be from your grade) in your team.")
        print(self.non_form_errors())


@login_required
def create_multiple_players(request):
    FootballPlayerFormSet = formset_factory(PlayerForm, extra=9, formset=FirstFiveRequiredFormset)
    if request.method == 'GET':
        formset = FootballPlayerFormSet()
        return render(request, 'team/add_players.html', {'formset': formset})
    else:
        formset = FootballPlayerFormSet(request.POST, form_kwargs={'user': request.user})
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
            return redirect('homepage')
        else:
            return render(request, 'team/add_players.html', {'formset': formset})
