from django.db import models
from django.contrib.auth.models import User
from albums.models import Album
from profiles.models import Profile
from instruments.models import Instrument
from django.utils.text import slugify
from django.db.models.signals import post_migrate


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Mood(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class ProjectType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Track(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('review', 'Ready for Review'),
        ('completed', 'Completed and Reviewed'),
    ]

    title = models.CharField(max_length=255, blank=False, null=False)
    notes = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='in_progress', blank=False, null=False)
    project_type = models.ForeignKey(
        ProjectType, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')

    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='tracks')
    mood = models.ForeignKey(Mood, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='tracks')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='album_tracks')
    instruments = models.ManyToManyField(
        Instrument, blank=True, related_name='instrument_tracks')
    assigned_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tracks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return f"{self.title} - {self.status} ({self.project_type})"


DEFAULT_GENRES = ["Orchestral", "Electronic", "Rock", "Soundtrack"]
DEFAULT_MOODS = ["Epic", "Mysterious", "Relaxing", "Hype"]
DEFAULT_PROJECT_TYPES = ["Trailer Music",
                         "Game Soundtrack", "Advertising", "Film Score"]


def populate_defaults(sender, **kwargs):
    # ✅ Import inside function to prevent circular errors
    from tracks.models import Genre, Mood, ProjectType

    for genre in DEFAULT_GENRES:
        Genre.objects.get_or_create(name=genre)
    for mood in DEFAULT_MOODS:
        Mood.objects.get_or_create(name=mood)
    for project_type in DEFAULT_PROJECT_TYPES:
        ProjectType.objects.get_or_create(name=project_type)


post_migrate.connect(populate_defaults)
