# Generated by Django 4.2.3 on 2023-08-11 12:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("match", "0005_matchplayerstats_remove_goal_match_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="matchplayerstats",
            options={"verbose_name_plural": "match player stats"},
        ),
    ]
