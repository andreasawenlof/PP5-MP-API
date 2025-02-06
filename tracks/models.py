from django.db import models
from django.contrib.auth.models import User
from albums.models import Album
from profiles.models import Profile
from instruments.models import Instrument
from django.utils.text import slugify
from django.db.models.signals import post_migrate
from django.core.exceptions import ValidationError


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Mood(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ProjectType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Track(models.Model):

    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_production', 'In Production'),
        ('ready_for_mixing', 'Ready for Mixing'),
        ('ready_for_review', 'Ready for Review'),
        ('completed_and_reviewed', 'Completed and Reviewed'),
    ]

    VOCALS_STATUS_CHOICES = [
        ('vocals_in_progress', 'In Progress'),
        ('vocals_done', 'Done'),
    ]

    title = models.CharField(max_length=255, blank=False, null=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_tracks"
    )
    notes = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=25, choices=STATUS_CHOICES, default='not_started', blank=False, null=False
    )

    vocals_needed = models.BooleanField(default=False)
    vocals_status = models.CharField(
        max_length=20,
        choices=VOCALS_STATUS_CHOICES,
        blank=True,
        null=True,
        default='vocals_in_progress'
    )

    project_type = models.ForeignKey(
        ProjectType, on_delete=models.SET_NULL, null=True, blank=True, related_name="project_tracks"
    )  # ✅ Updated related_name

    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name="genre_tracks"
    )  # ✅ Updated related_name

    mood = models.ForeignKey(
        Mood, on_delete=models.SET_NULL, null=True, blank=True, related_name="mood_tracks"
    )  # ✅ Updated related_name

    album = models.ForeignKey(
        Album, on_delete=models.SET_NULL, null=True, blank=True, related_name="album_tracks"
    )
    instruments = models.ManyToManyField(
        Instrument, blank=True, related_name="instrument_tracks"
    )
    assigned_composer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tracks"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    @property
    def status_display(self):
        return self.get_status_display()

    def __str__(self):
        return f"{self.title} - {self.status} ({self.project_type})"

    def save(self, *args, **kwargs):
        if not self.vocals_needed:
            self.vocals_status = None
        elif self.vocals_status is None:
            self.vocals_status = 'vocals_in_progress'
        super().save(*args, **kwargs)

    def set_review_status(self, new_status):
        if self.status == 'ready_for_review':
            self.review_status = new_status
            self.save()
        else:
            raise ValidationError(
                "Review status can only be changed when the track is ready for review.")

    @classmethod
    def bulk_update_tracks(cls, track_ids, **kwargs):
        """
        Bulk update tracks with the given IDs.

        :param track_ids: List of track IDs to update
        :param kwargs: Fields to update and their new values
        """
        tracks = cls.objects.filter(id__in=track_ids)

        # Validate the status if it's being updated
        if 'status' in kwargs and kwargs['status'] not in dict(cls.STATUS_CHOICES):
            raise ValueError("Invalid status")

        # Validate the vocals_status if it's being updated
        if 'vocals_status' in kwargs and kwargs['vocals_status'] not in dict(cls.VOCALS_STATUS_CHOICES):
            raise ValueError("Invalid vocals status")

        # Handle special case for vocals_needed
        if 'vocals_needed' in kwargs and not kwargs['vocals_needed']:
            kwargs['vocals_status'] = None

        tracks.update(**kwargs)
