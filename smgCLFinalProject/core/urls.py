from django.urls import path
from . import views

urlpatterns = [
    path("", views.Homepage.as_view(), name="homepage"),
    path("about-us/", views.AboutUs.as_view(), name="about us"),
]
