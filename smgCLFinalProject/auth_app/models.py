from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, User
from django.db import models


class CaptainUser(AbstractUser):
    grade = models.CharField(max_length=2,
                             choices=[('', 'Grade'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')])
    paralelka = models.CharField(max_length=1,
                                 choices=[('', 'Class'), ('A', 'A'), ('B', 'B'), ('V', 'V'), ('G', 'G'), ('D', 'D'),
                                          ('E', 'E')], )
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=False)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
