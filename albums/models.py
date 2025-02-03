from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


class Album(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('review', 'Ready for Review'),
        ('completed', 'Completed and Reviewed'),
    ]

    title = models.CharField(max_length=255, blank=False, null=False)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='in_progress'
    )
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
        Automatically updates the status of all tracks in this album
        when the album status is changed.
        """
        from tracks.models import Track  # Lazy import to avoid circular import issues

        # ✅ Get tracks that belong to this album
        tracks = Track.objects.filter(album=self)

        # ✅ Save the album first
        super().save(*args, **kwargs)

        # ✅ Only update tracks if necessary
        if tracks.exists():
            tracks_to_update = []
            for track in tracks:
                if track.status != self.status:  # ✅ Only update if status changed
                    track.status = self.status
                    tracks_to_update.append(track)

            # ✅ Optimized DB update (only updates changed tracks)
            if tracks_to_update:
                Track.objects.bulk_update(tracks_to_update, ['status'])
