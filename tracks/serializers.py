from rest_framework import serializers
from .models import Track, Genre, Mood, ProjectType
from albums.models import Album
from instruments.models import Instrument
from django.contrib.auth.models import User


# ✅ Independent Serializers for Mood, Genre, and ProjectType
class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = "__all__"


class TrackSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(), allow_null=True
    )
    instruments = serializers.SlugRelatedField(
        queryset=Instrument.objects.all(),
        slug_field="name",
        many=True,  # ✅ NOW ALLOWS MULTIPLE INSTRUMENTS
        required=False
    )

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="name"
    )
    mood = serializers.SlugRelatedField(
        queryset=Mood.objects.all(), slug_field="name"
    )
    project_type = serializers.SlugRelatedField(
        queryset=ProjectType.objects.all(), slug_field="name"
    )

    status = serializers.ReadOnlyField(source="get_status_display")
    assigned_user = serializers.ReadOnlyField(source="assigned_user.username")

    class Meta:
        model = Track
        fields = "__all__"

    def create(self, validated_data):
        """Ensure the assigned user is set to the creator if not provided."""
        if "assigned_user" not in validated_data:
            validated_data["assigned_user"] = self.context["request"].user
        return super().create(validated_data)
