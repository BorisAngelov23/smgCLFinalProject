# Generated by Django 4.2.3 on 2023-07-23 10:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("team", "0002_team_captain_team_grade_team_paralelki_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="team",
            old_name="team_name",
            new_name="name",
        ),
    ]
