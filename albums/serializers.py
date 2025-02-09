from rest_framework import serializers
from django.db import transaction
from .models import Album
from tracks.models import Track, Genre, Mood, ProjectType


class SimpleTrackSerializer(serializers.ModelSerializer):
    """Used in album list view to show a lightweight version of tracks."""

    class Meta:
        model = Track
        fields = ["id", "title"]


class DetailedTrackSerializer(serializers.ModelSerializer):
    """Used in album detail view to provide full track details."""

    instruments = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=True
    )

    class Meta:
        model = Track
        fields = [
            "id",
            "title",
            "album",
            "instruments",
            "status",
            "vocals_needed",
            "vocals_status",
            "assigned_composer",
            "notes",
            "created_at",
            "updated_at",
        ]


class AlbumSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="name", required=False, allow_null=True
    )
    mood = serializers.SlugRelatedField(
        queryset=Mood.objects.all(), slug_field="name", required=False, allow_null=True
    )
    project_type = serializers.SlugRelatedField(
        queryset=ProjectType.objects.all(),
        slug_field="name",
        required=False,
        allow_null=True,
    )

    tracks = serializers.SerializerMethodField()
    track_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Track.objects.all(), required=False, write_only=True
    )

    class Meta:
        model = Album
        fields = [
            "id",
            "title",
            "owner",
            "status",
            "cover_art",
            "notes",
            "project_type",
            "genre",
            "mood",
            "created_at",
            "updated_at",
            "tracks",
            "track_ids",
        ]

    def get_tracks(self, obj):
        """
        If we're in Album Detail View, return full track details.
        If we're in Album List View, return only track ID & title.
        """
        serializer_class = (
            DetailedTrackSerializer
            if self.context.get("is_detail", False)
            else SimpleTrackSerializer
        )
        return serializer_class(obj.tracks.all(), many=True).data

    def to_representation(self, instance):
        """Ensure track_ids are **ALWAYS** included in the response."""
        data = super().to_representation(instance)
        data["track_ids"] = list(
            instance.tracks.values_list("id", flat=True)
        )  # ✅ Fix for preselected tracks
        return data

    @transaction.atomic
    def create(self, validated_data):
        """Creates a new album and assigns tracks if provided."""
        track_ids = validated_data.pop("track_ids", [])
        owner = self.context["request"].user
        album = Album.objects.create(owner=owner, **validated_data)
        album.tracks.set(track_ids)
        return album

    @transaction.atomic
    def update(self, instance, validated_data):
        """Updates album details while keeping existing tracks unless changed."""
        track_ids = validated_data.pop("track_ids", None)

        # Update album fields normally
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if track_ids is not None:  # ✅ Only update tracks if track_ids were provided
            instance.tracks.set(track_ids)

        return instance
