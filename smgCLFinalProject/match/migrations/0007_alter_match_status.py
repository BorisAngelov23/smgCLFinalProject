# Generated by Django 4.2.3 on 2023-12-17 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0006_alter_matchplayerstats_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined'), ('live', 'Live'), ('played', 'Played')], default='pending', max_length=10),
        ),
    ]
