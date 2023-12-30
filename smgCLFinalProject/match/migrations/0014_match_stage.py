# Generated by Django 4.2.3 on 2023-12-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0013_remove_matchplayerstats_minute_of_goal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='stage',
            field=models.CharField(choices=[('Round 1', 'Round 1'), ('Round 2', 'Round 2'), ('Round 3', 'Round 3'), ('Play-offs', 'Play-offs'), ('Quarter-finals', 'Quarter-finals'), ('Semi-finals', 'Semi-finals'), ('Final', 'Final')], default='Round 1', max_length=20),
        ),
    ]