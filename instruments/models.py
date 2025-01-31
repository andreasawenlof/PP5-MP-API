from django.db import models
from cloudinary.models import CloudinaryField


class InstrumentCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Instrument(models.Model):
    name = models.CharField(max_length=255, unique=True)
    categories = models.ManyToManyField(
        InstrumentCategory, related_name="instruments")
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
