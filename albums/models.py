from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.apps import apps


class Album(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=255, blank=False, null=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='albums')
    status = models.CharField(
        max_length=25, choices=STATUS_CHOICES, default='not_started')
    cover_art = CloudinaryField('image', blank=True, null=True)
    notes = models.TextField(blank=True, default="")

    project_type = models.ForeignKey(
        "tracks.ProjectType", on_delete=models.SET_NULL, null=True, blank=True
    )
    genre = models.ForeignKey(
        "tracks.Genre", on_delete=models.SET_NULL, null=True, blank=True
    )
    mood = models.ForeignKey(
        "tracks.Mood", on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} - {self.status}"

    def save(self, *args, **kwargs):
        """
        Automatically updates the status, project_type, genre, and mood of all tracks 
        in this album when the album is changed.
        """
        # Get the current state of the album from the database
        if self.pk:
            old_album = Album.objects.get(pk=self.pk)
            fields_to_update = []

            if old_album.status != self.status:
                fields_to_update.append('status')
            if old_album.project_type != self.project_type:
                fields_to_update.append('project_type')
            if old_album.genre != self.genre:
                fields_to_update.append('genre')
            if old_album.mood != self.mood:
                fields_to_update.append('mood')

        # Save the album first
        super().save(*args, **kwargs)

        # Update associated tracks if necessary
        if self.pk and fields_to_update:
            Track = apps.get_model('tracks', 'Track')
            tracks = Track.objects.filter(album=self)
            if tracks.exists():
                tracks_to_update = []
                for track in tracks:
                    updated = False
                    for field in fields_to_update:
                        if getattr(track, field) != getattr(self, field):
                            setattr(track, field, getattr(self, field))
                            updated = True
                    if updated:
                        tracks_to_update.append(track)

                # Optimized DB update (only updates changed tracks)
                if tracks_to_update:
                    Track.objects.bulk_update(
                        tracks_to_update, fields_to_update)
