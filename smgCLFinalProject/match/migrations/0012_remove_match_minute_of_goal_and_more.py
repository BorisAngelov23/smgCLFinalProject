# Generated by Django 4.2.3 on 2023-12-20 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0011_rename_minute_of_event_match_minute_of_goal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='minute_of_goal',
        ),
        migrations.AddField(
            model_name='matchplayerstats',
            name='minute_of_goal',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
