from django.views.generic import ListView, DetailView

from smgCLFinalProject.article.models import Article

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ArticleListView(ListView):
    template_name = "article/all_articles.html"
    model = Article
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.all().order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = context['articles']

        paginator = Paginator(articles, 8)
        page = self.request.GET.get('page')

        try:
            context['articles'] = paginator.page(page)
        except PageNotAnInteger:
            context['articles'] = paginator.page(1)
        except EmptyPage:
            context['articles'] = paginator.page(paginator.num_pages)

        return context


class ArticleDetailView(DetailView):
    template_name = "article/article.html"
    model = Article
    context_object_name = "article"
