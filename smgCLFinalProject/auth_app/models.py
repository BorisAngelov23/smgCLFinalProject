from django.contrib.auth.models import AbstractUser
from django.db import models


class CaptainUser(AbstractUser):
    grade = models.CharField(max_length=2, choices=[('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')])
    paralelka = models.CharField(max_length=1, choices=[('А', 'А'), ('Б', 'Б'), ('В', 'В'), ('Г', 'Г'), ('Д', 'Д'), ('Е', 'Е')])
    phone_number = models.CharField(max_length=10, null=True, blank=True)
