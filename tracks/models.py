from django.db import models
from django.contrib.auth.models import User
from albums.models import Album
from profiles.models import Profile


class Track(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('review', 'Ready for Review'),
        ('completed', 'Completed and Reviewed'),
    ]

    PROJECT_TYPE = [
        ('quantity', 'Quantity'),
        ('quality', 'Quality'),
        ('custom', 'Custom Work'),
        ('other', 'Other'),
    ]

    GENRE_CHOICES = [
        ('rock', 'Rock'),
        ('pop', 'Pop'),
        ('electronic', 'Electronic'),
        ('soundtrack', 'Soundtrack'),
        ('other', 'Other'),
    ]

    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('energetic', 'Energetic'),
        ('relaxed', 'Relaxed'),
        ('dramatic', 'Dramatic'),
        ('hype', 'Hype'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255, blank=False, null=False)
    notes = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='in_progress', blank=False, null=False)
    project_type = models.CharField(
        max_length=20, choices=PROJECT_TYPE, default='quantity', blank=False, null=False)
    genre = models.CharField(
        max_length=20, choices=GENRE_CHOICES, blank=False, null=False, default='other')
    mood = models.CharField(
        max_length=20, choices=MOOD_CHOICES, blank=False, null=False, default='other')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='album_tracks')
    instruments = models.ManyToManyField(
        'Instrument', blank=True, related_name='instrument_tracks')
    assigned_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tracks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return f"{self.title} - {self.status} ({self.project_type})"


class Instrument(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            blank=False, null=False)

    def __str__(self):
        return f"{self.name}"
