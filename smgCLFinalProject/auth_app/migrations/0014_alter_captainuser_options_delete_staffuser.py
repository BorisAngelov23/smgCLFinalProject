# Generated by Django 4.2.3 on 2023-08-11 16:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auth_app", "0013_alter_captainuser_options_staffuser"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="captainuser",
            options={"verbose_name": "user", "verbose_name_plural": "users"},
        ),
        migrations.DeleteModel(
            name="StaffUser",
        ),
    ]
