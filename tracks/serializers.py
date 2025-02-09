from rest_framework import serializers
from .models import Track, Genre, Mood, ProjectType
from albums.models import Album
from instruments.models import Instrument
from django.contrib.auth.models import User

# Reusable serializers


class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ["id", "name"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ["id", "name"]


# Main Track Serializer


class TrackSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    album = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(), allow_null=True
    )
    album_name = serializers.CharField(source="album.title", read_only=True)

    instruments = serializers.PrimaryKeyRelatedField(
        queryset=Instrument.objects.all(), many=True, required=False
    )
    instrument_names = serializers.SlugRelatedField(
        source="instruments", slug_field="name", many=True, read_only=True
    )

    genre = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), allow_null=True
    )
    genre_name = serializers.CharField(source="genre.name", read_only=True)

    mood = serializers.PrimaryKeyRelatedField(
        queryset=Mood.objects.all(), allow_null=True
    )
    mood_name = serializers.CharField(source="mood.name", read_only=True)

    project_type = serializers.PrimaryKeyRelatedField(
        queryset=ProjectType.objects.all(), allow_null=True
    )
    project_type_name = serializers.CharField(
        source="project_type.name", read_only=True
    )

    assigned_composer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(profile__is_composer=True),
        required=False,
        allow_null=True,
    )
    assigned_composer_username = serializers.CharField(
        source="assigned_composer.username", read_only=True
    )

    status_display = serializers.CharField(read_only=True)

    class Meta:
        model = Track
        fields = [
            "id",
            "owner",
            "title",
            "album",
            "album_name",
            "instruments",
            "instrument_names",
            "genre",
            "genre_name",
            "mood",
            "mood_name",
            "project_type",
            "project_type_name",
            "status",
            "status_display",
            "vocals_needed",
            "vocals_status",
            "assigned_composer",
            "assigned_composer_username",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["owner"]

    def update(self, instance, validated_data):
        # Handle instruments
        if "instruments" in validated_data:
            instance.instruments.set(validated_data.pop("instruments"))

        # Update all other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# Bulk Update Serializer (Ensure this is at the bottom)


class BulkTrackUpdateSerializer(serializers.Serializer):
    track_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )
    status = serializers.ChoiceField(choices=Track.STATUS_CHOICES, required=False)
    vocals_needed = serializers.BooleanField(required=False)
    vocals_status = serializers.ChoiceField(
        choices=Track.VOCALS_STATUS_CHOICES, allow_null=True, required=False
    )
    album = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(), allow_null=True, required=False
    )
    genre = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), allow_null=True, required=False
    )
    mood = serializers.PrimaryKeyRelatedField(
        queryset=Mood.objects.all(), allow_null=True, required=False
    )
    project_type = serializers.PrimaryKeyRelatedField(
        queryset=ProjectType.objects.all(), allow_null=True, required=False
    )

    def validate(self, data):
        """Ensure at least one field besides track_ids is being updated"""
        if len(data) == 1:
            raise serializers.ValidationError(
                "At least one field to update must be provided."
            )
        return data

    def update(self, instance, validated_data):
        """Perform bulk update while ensuring assigned_composer is untouched"""
        track_ids = validated_data.pop("track_ids")

        # Prevent assigned_composer updates in bulk
        if "assigned_composer" in validated_data:
            validated_data.pop("assigned_composer")

        Track.bulk_update_tracks(track_ids, **validated_data)
        return Track.objects.filter(id__in=track_ids)
