from django.contrib import admin
from .models import Match, MatchPlayerStats
from .forms import MatchForm


class MatchPlayerStatsInline(admin.TabularInline):
    model = MatchPlayerStats
    extra = 1
    fields = ('player', 'goals_scored', 'minutes_of_goal', 'assists', 'yellow_cards', 'red_cards')

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            team1_players = obj.team1.players.all()
            team2_players = obj.team2.players.all()
            valid_players = team1_players | team2_players
            formset.form.base_fields["player"].queryset = valid_players
        return formset


class MatchAdmin(admin.ModelAdmin):
    form = MatchForm
    inlines = [MatchPlayerStatsInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if form.instance.status != "declined":
            players_stats = form.instance.matchplayerstats_set.all()
            for player_stat in players_stats:
                player = player_stat.player
                player.goals = 0
                player.assists = 0
                player.yellow_cards = 0
                player.red_cards = 0
                for match_stats in MatchPlayerStats.objects.filter(player=player):
                    player.goals += match_stats.goals_scored
                    player.assists += match_stats.assists
                    player.yellow_cards += match_stats.yellow_cards
                    player.red_cards += match_stats.red_cards
                player.save()


admin.site.register(Match, MatchAdmin)
