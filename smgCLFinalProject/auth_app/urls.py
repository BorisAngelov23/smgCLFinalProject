from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CaptainRegister.as_view(), name='captain_register'),
    path('login/', views.CaptainLogin.as_view(), name='captain_login'),
    path('logout/', views.CaptainLogout.as_view(), name='captain_logout'),
    path('details/<int:pk>', views.CaptainDetails.as_view(), name='captain_details'),
    path('edit/<int:pk>', views.CaptainEdit.as_view(), name='captain_edit'),
]
