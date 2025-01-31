from django.db import models
from tracks.models import Track
from django.contrib.auth.models import User


class Review(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('needs_revision', 'Needs Revision'),
    ]

    track = models.ForeignKey(
        Track, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(
        User, related_name='reviews', on_delete=models.CASCADE)
    feedback = models.TextField()
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reviewed_at']

    def __str__(self):
        return f"Review for {self.track.title} by {self.reviewer.username}"


class ReviewHistory(models.Model):
    review = models.ForeignKey(
        Review, related_name="history", on_delete=models.CASCADE)
    editor = models.ForeignKey(
        User, related_name="review_edits", on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now_add=True)
    updated_feedback = models.TextField()  # Updated feedback text after revisions
    revision_number = models.IntegerField(default=1)

    class Meta:
        ordering = ['-edited_at']

    def __str__(self):
        return f"Revision {self.revision_number} for {self.review.track.title}"
