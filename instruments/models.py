from django.db import models
from cloudinary.models import CloudinaryField


class InstrumentCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]  # ✅ Always return categories in alphabetical order

    def __str__(self):
        return f"{self.name}"


class Instrument(models.Model):
    name = models.CharField(max_length=255, unique=True)
    categories = models.ManyToManyField(InstrumentCategory, related_name="instruments")
    image = CloudinaryField("image", blank=True, null=True)

    class Meta:
        # ✅ Always return instruments in alphabetical order
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
