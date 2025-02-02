from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.apps import apps


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

    def get_project_type(self):
        return apps.get_model('tracks', 'ProjectType')

    def get_genre(self):
        return apps.get_model('tracks', 'Genre')

    def get_mood(self):
        return apps.get_model('tracks', 'Mood')

    project_type = models.ForeignKey(
        'tracks.ProjectType', on_delete=models.SET_NULL, null=True, blank=True
    )
    genre = models.ForeignKey(
        'tracks.Genre', on_delete=models.SET_NULL, null=True, blank=True
    )
    mood = models.ForeignKey(
        'tracks.Mood', on_delete=models.SET_NULL, null=True, blank=True
    )

    # ✅ FIXED: Added a ManyToMany relationship for assigning tracks
    tracks = models.ManyToManyField(
        "tracks.Track", blank=True, related_name="albums")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} - {self.status}"

    def add_track(self, track):
        """✅ FIX: Import `Track` here to avoid circular import"""
        from tracks.models import Track  # ✅ Lazy import to prevent circular import
        if isinstance(track, Track):
            self.tracks.add(track)
