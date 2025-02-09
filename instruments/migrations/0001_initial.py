# Generated by Django 4.2.18 on 2025-01-31 06:54

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="InstrumentCategory",
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
                ("name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Instrument",
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
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "image",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        related_name="instruments", to="instruments.instrumentcategory"
                    ),
                ),
            ],
        ),
    ]
