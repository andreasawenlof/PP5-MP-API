from django.db import models
from django.contrib.auth.models import User
from tracks.models import Track
from albums.models import Album


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments")
    track = models.ForeignKey(
        Track, related_name="track_comments", on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name="album_comments",
                              on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.track.title}"

    class Meta:
        ordering = ['-created_at']
