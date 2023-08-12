from django.urls import path

from smgCLFinalProject.article import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='all_articles'),
    path('<int:pk>', views.ArticleDetailView.as_view(), name='article'),
]
