from django.contrib import admin
from .models import Match, MatchPlayerStats


class MatchPlayerStatsInline(admin.TabularInline):
    model = MatchPlayerStats
    extra = 0


class MatchAdmin(admin.ModelAdmin):
    inlines = [MatchPlayerStatsInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if form.instance.status != 'declined':
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
