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


# ✅ Main TrackSerializer
class TrackSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(), allow_null=True
    )
    instruments = serializers.SlugRelatedField(
        queryset=Instrument.objects.all(),
        slug_field="name",  # ✅ Displays instrument names instead of IDs
        many=True,  # ✅ Allows selecting multiple instruments
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

    status = serializers.ChoiceField(  # ✅ Can now be updated!
        choices=Track.STATUS_CHOICES
    )
    assigned_user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
        required=False  # ✅ Optional, so it defaults if not provided
    )

    class Meta:
        model = Track
        fields = "__all__"

        fields = [
            "title",
            "album",
            "instruments",
            "genre",
            "mood",
            "project_type",
            "status",
            "assigned_user",
            "notes",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """✅ Ensure the assigned user is set to the creator if not provided."""
        if "assigned_user" not in validated_data:
            validated_data["assigned_user"] = self.context["request"].user

        # ✅ Fix: Handle ManyToMany Instruments properly
        instruments_data = validated_data.pop("instruments", [])
        track = super().create(validated_data)
        track.instruments.set(instruments_data)  # ✅ Add multiple instruments
        return track

    def update(self, instance, validated_data):
        """✅ Allow updating instruments & status properly in tracks."""
        if "instruments" in validated_data:
            instance.instruments.set(validated_data.pop(
                "instruments"))  # ✅ Proper ManyToMany update

        return super().update(instance, validated_data)
