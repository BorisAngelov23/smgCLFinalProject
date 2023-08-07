# Generated by Django 4.2.3 on 2023-07-23 11:39

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_rename_team_name_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='paralelki',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1), choices=[('', 'Class'), ('A', 'A'), ('B', 'B'), ('V', 'V'), ('G', 'G'), ('D', 'D'), ('E', 'E')], default=None, max_length=1, size=3),
        ),
    ]
