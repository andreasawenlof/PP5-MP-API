# Generated by Django 4.2.18 on 2025-02-03 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0004_album_tracks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='status',
            field=models.CharField(choices=[('not_started', 'Not Started'), ('in_production', 'In Production'), ('ready_for_mixing', 'Ready for Mixing'), ('ready_for_review', 'Ready for Review'), ('completed_and_reviewed', 'Completed and Reviewed')], default='not_started', max_length=25),
        ),
    ]
