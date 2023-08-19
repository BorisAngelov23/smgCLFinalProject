from django.views.generic import ListView, DetailView

from smgCLFinalProject.article.models import Article


class ArticleListView(ListView):
    template_name = "article/all_articles.html"
    model = Article
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.all().order_by("-date")


class ArticleDetailView(DetailView):
    template_name = "article/article.html"
    model = Article
    context_object_name = "article"
