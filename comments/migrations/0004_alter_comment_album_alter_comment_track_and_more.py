# Generated by Django 4.2.18 on 2025-02-03 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0004_remove_track_comments'),
        ('albums', '0002_alter_album_options_album_notes_alter_album_genre_and_more'),
        ('comments', '0003_remove_comment_author_comment_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='albums.album'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tracks.track'),
        ),
        migrations.AddConstraint(
            model_name='comment',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('album__isnull', True), ('track__isnull', False)), models.Q(('album__isnull', False), ('track__isnull', True)), _connector='OR'), name='comment_track_xor_album'),
        ),
    ]
