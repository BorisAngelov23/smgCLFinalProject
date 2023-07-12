from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CaptainRegister.as_view(), name='captain_register'),
]
