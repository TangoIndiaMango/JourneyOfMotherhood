# Generated by Django 4.1.7 on 2023-05-08 16:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="read",
            field=models.BooleanField(default=False),
        ),
    ]
