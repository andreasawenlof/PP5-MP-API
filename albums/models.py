from django.db import models
from cloudinary.models import CloudinaryField


class Album(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('review', 'Ready for Review'),
        ('completed', 'Completed and Reviewed'),
    ]

    PROJECT_TYPE_CHOICES = [
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
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='in_progress', blank=False, null=False)
    cover_art = CloudinaryField('image', blank=True, null=True)
    project_type = models.CharField(
        max_length=20, choices=PROJECT_TYPE_CHOICES, default='quantity', blank=False, null=False)
    genre = models.CharField(
        max_length=20, choices=GENRE_CHOICES, blank=False, null=False, default='other')
    mood = models.CharField(
        max_length=20, choices=MOOD_CHOICES, blank=False, null=False, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return f"{self.title} - {self.status} ({self.project_type})"
