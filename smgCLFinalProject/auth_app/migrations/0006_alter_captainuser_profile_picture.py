# Generated by Django 4.2.3 on 2023-07-13 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0005_alter_captainuser_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='captainuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='media/profile_pictures/'),
        ),
    ]
