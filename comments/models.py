from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from tracks.models import Track
from albums.models import Album


class Comment(models.Model):
    """A single comment linked to either a Track OR an Album (not both)."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    track = models.ForeignKey(
        Track,
        related_name="comments",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    album = models.ForeignKey(
        Album,
        related_name="comments",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(track__isnull=False, album__isnull=True) |
                    models.Q(track__isnull=True, album__isnull=False)
                ),
                name='comment_track_xor_album'
            )
        ]

    def clean(self):
        if self.track and self.album:
            raise ValidationError(
                "A comment can only be associated with either a track or an album, not both.")
        if not self.track and not self.album:
            raise ValidationError(
                "A comment must be associated with either a track or an album.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.track:
            return f"Comment on Track: {self.track.title}"  # pylint: disable=no-member

        elif self.album:  # pylint: disable=no-member

            return f"Comment on Album: {self.album.title}"  # pylint: disable=no-member

        return f"Comment by {self.owner.username}"  # pylint: disable=no-member
