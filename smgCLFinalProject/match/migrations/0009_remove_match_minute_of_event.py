# Generated by Django 4.2.3 on 2023-12-19 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0008_match_minute_of_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='minute_of_event',
        ),
    ]