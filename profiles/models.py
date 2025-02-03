from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save


class Profile(models.Model):
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_composer = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)
    avatar = CloudinaryField(
        'image', blank=True, null=True, default='default_profile_lhtmj4')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.display_name}"


def create_profile(sender, instance, created, **kwargs):
    """
    Create profile
    """
    if created:
        Profile.objects.create(owner=instance, display_name=instance.username)


post_save.connect(create_profile, sender=User)
