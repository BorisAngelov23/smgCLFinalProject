from django.urls import path
from . import views

urlpatterns = [
    path('arrange/', views.ArrangeMatch.as_view(), name='arrange_match'),
    path('respond/<int:pk>/', views.MatchResponse.as_view(), name='respond_to_match'),
    path('request-sent/', views.MatchRequestSent.as_view(), name='match_request_sent'),
    path('api/match_goalscorers/<int:match_id>/', views.MatchGoalscorersView.as_view(), name='match_goalscorers_api'),
    path('all/', views.MatchesTemplateView.as_view(), name='matches'),

]
