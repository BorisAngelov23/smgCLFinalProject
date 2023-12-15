from django.views.generic import TemplateView

from smgCLFinalProject.article.models import Article
from smgCLFinalProject.match.models import Match


class Homepage(TemplateView):
    template_name = "core/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.added_players:
            context["match"] = Match.objects.filter(
                team2=self.request.user.team, status="pending"
            ).first()
        context["articles"] = Article.objects.all()
        return context


class AboutUs(TemplateView):
    template_name = "core/about_us.html"
