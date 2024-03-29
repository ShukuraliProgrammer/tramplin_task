# Generated by Django 5.0.1 on 2024-01-24 07:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                    "username",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="username"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator("^\\+?[1-9]\\d{11}$")
                        ],
                        verbose_name="phone",
                    ),
                ),
            ],
            options={
                "verbose_name": "profile",
                "verbose_name_plural": "profiles",
            },
        ),
    ]
