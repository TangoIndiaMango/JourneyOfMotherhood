# Generated by Django 4.1.7 on 2023-03-06 06:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="email address"
                    ),
                ),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("M", "Male"),
                            ("F", "Female"),
                            ("O", "Rather not say"),
                        ],
                        max_length=1,
                    ),
                ),
                ("date_of_birth", models.DateField()),
                (
                    "profile_pic",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_pictures/"
                    ),
                ),
                ("about_me", models.TextField(blank=True, max_length=500, null=True)),
                ("post_count", models.PositiveIntegerField(default=0)),
                ("followers_count", models.PositiveIntegerField(default=0)),
                ("following_count", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "following",
                    models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
