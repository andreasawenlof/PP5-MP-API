# Generated by Django 4.2.18 on 2025-02-03 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0005_rename_assigned_user_track_assigned_composer_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='track',
            options={'ordering': ['-updated_at']},
        ),
    ]
