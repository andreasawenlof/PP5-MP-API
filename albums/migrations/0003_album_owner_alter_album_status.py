# Generated by Django 4.2.18 on 2025-02-03 06:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("albums", "0002_alter_album_options_album_notes_alter_album_genre_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="album",
            name="owner",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="albums",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="album",
            name="status",
            field=models.CharField(
                choices=[
                    ("not_started", "Not Started"),
                    ("in_progress", "In Progress"),
                    ("completed", "Completed"),
                    ("on_hold", "On Hold"),
                    ("cancelled", "Cancelled"),
                ],
                default="not_started",
                max_length=25,
            ),
        ),
    ]
