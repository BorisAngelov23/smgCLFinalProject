# Generated by Django 4.2.3 on 2023-08-11 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0013_player_mvps'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ('grade', 'paralelka', 'first_name', 'last_name')},
        ),
    ]
