from django.urls import path
from . import views

urlpatterns = [
    path('arrange/', views.ArrangeMatch.as_view(), name='arrange_match'),
    path('respond/<int:pk>/', views.MatchResponse.as_view(), name='respond_to_match'),
    path('request-sent/', views.MatchRequestSent.as_view(), name='match_request_sent'),
    path('', views.AllMatchesList.as_view(), name='matches'),
]
