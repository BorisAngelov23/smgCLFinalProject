# Generated by Django 4.2.3 on 2023-07-13 08:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="captainuser",
            name="paralelka",
            field=models.CharField(
                choices=[
                    ("A", "A"),
                    ("B", "B"),
                    ("V", "V"),
                    ("G", "G"),
                    ("D", "D"),
                    ("E", "E"),
                ],
                max_length=1,
            ),
        ),
    ]
