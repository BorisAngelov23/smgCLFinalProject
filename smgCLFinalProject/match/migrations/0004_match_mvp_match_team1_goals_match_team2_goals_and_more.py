# Generated by Django 4.2.3 on 2023-08-11 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("team", "0012_team_goal_difference"),
        ("match", "0003_alter_match_team1_alter_match_team2"),
    ]

    operations = [
        migrations.AddField(
            model_name="match",
            name="mvp",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="team.player",
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="team1_goals",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="match",
            name="team2_goals",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="match",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("accepted", "Accepted"),
                    ("declined", "Declined"),
                    ("played", "Played"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="YellowCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "match",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="yellow_cards",
                        to="match.match",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="team.player"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RedCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "match",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="red_cards",
                        to="match.match",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="team.player"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Goal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "match",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="goals",
                        to="match.match",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="team.player"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Assist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "match",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assists",
                        to="match.match",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="team.player"
                    ),
                ),
            ],
        ),
    ]
