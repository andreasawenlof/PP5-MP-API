from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.apps import apps


class Album(models.Model):
    STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("in_production", "In Production"),
        ("ready_for_mixing", "Ready for Mixing"),
        ("ready_for_review", "Ready for Review"),
        ("completed_and_reviewed", "Completed and Reviewed"),
    ]

    title = models.CharField(max_length=255, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="albums")
    status = models.CharField(
        max_length=25, choices=STATUS_CHOICES, default="not_started"
    )
    cover_art = CloudinaryField("image", blank=True, null=True)
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
    tracks = models.ManyToManyField("tracks.Track", related_name="albums", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.title} - {self.status}"

    def save(self, *args, **kwargs):
        """Auto-updates the status, project_type, genre, and mood of all tracks in this album"""
        is_new = self._state.adding
        fields_to_update = []

        if not is_new:
            old_album = Album.objects.get(pk=self.pk)
            for field in ["status", "project_type", "genre", "mood"]:
                if getattr(old_album, field) != getattr(self, field):
                    fields_to_update.append(field)

        super().save(*args, **kwargs)

        Track = apps.get_model("tracks", "Track")

        if fields_to_update:
            tracks_to_update = list(self.tracks.all())
            for track in tracks_to_update:
                for field in fields_to_update:
                    setattr(track, field, getattr(self, field))
                track.album = self  # Maintain album relationship
            Track.objects.bulk_update(tracks_to_update, fields_to_update + ["album"])
