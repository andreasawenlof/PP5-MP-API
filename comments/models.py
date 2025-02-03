from django.db import models
from django.contrib.auth.models import User
from tracks.models import Track
from albums.models import Album


class Comment(models.Model):
    """A single comment linked to either a Track OR an Album (not both)."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    content = models.TextField()

    track = models.ForeignKey(
        Track,
        related_name="track_comments",
        on_delete=models.CASCADE, null=True, blank=True
    )
    album = models.ForeignKey(Album,
                              related_name="album_comments",
                              on_delete=models.CASCADE, null=True, blank=True
                              )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        author_name = self.author.username if self.author else "Unknown User"
        track_title = self.track.title if self.track_id else "No Track"
        album_title = self.album.title if self.album_id else "No Album"

        if self.track_id:
            return f"Comment by {author_name} on Track: {track_title}"
        elif self.album_id:
            return f"Comment by {author_name} on Album: {album_title}"
        return f"Comment by {author_name}"
