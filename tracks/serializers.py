from rest_framework import serializers
from .models import Track, Genre, Mood, ProjectType
from albums.models import Album
from instruments.models import Instrument
from django.contrib.auth.models import User


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
    owner = serializers.ReadOnlyField(source='owner.username')
    assigned_composer = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(profile__is_composer=True),
        required=False,
        allow_null=True
    )
    album = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(), allow_null=True
    )
    instruments = serializers.SlugRelatedField(
        queryset=Instrument.objects.all(),
        slug_field="name",
        many=True,
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
    status = serializers.ChoiceField(choices=Track.STATUS_CHOICES)
    vocals_status = serializers.ChoiceField(
        choices=Track.VOCALS_STATUS_CHOICES, allow_null=True, required=False)

    class Meta:
        model = Track
        fields = [
            "id", "owner", "title", "album", "instruments", "genre", "mood", "project_type",
            "status", "vocals_needed", "vocals_status", "assigned_composer",
            "notes", "created_at", "updated_at",
        ]

    def validate(self, data):
        vocals_needed = data.get('vocals_needed')
        vocals_status = data.get('vocals_status')

        # If this is an update, get the current values if not provided
        if self.instance:
            vocals_needed = vocals_needed if vocals_needed is not None else self.instance.vocals_needed
            vocals_status = vocals_status if 'vocals_status' in data else self.instance.vocals_status

        if vocals_needed is False:
            if vocals_status is not None:
                raise serializers.ValidationError(
                    "Cannot set vocals_status when vocals are not needed.")
            data['vocals_status'] = None
        elif vocals_needed is True and vocals_status is None:
            data['vocals_status'] = 'vocals_in_progress'

        return data

    def create(self, validated_data):
        instruments_data = validated_data.pop("instruments", [])

        # Ensure assigned_composer is set
        if "assigned_composer" not in validated_data:
            validated_data["assigned_composer"] = self.context["request"].user

        # Create the track instance
        track = Track.objects.create(**validated_data)

        # Set the instruments
        track.instruments.set(instruments_data)

        return track

    def update(self, instance, validated_data):
        if "instruments" in validated_data:
            instance.instruments.set(validated_data.pop("instruments"))
        return super().update(instance, validated_data)


class BulkTrackUpdateSerializer(serializers.Serializer):
    track_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    status = serializers.ChoiceField(
        choices=Track.STATUS_CHOICES, required=False)
    vocals_needed = serializers.BooleanField(required=False)
    vocals_status = serializers.ChoiceField(
        choices=Track.VOCALS_STATUS_CHOICES, allow_null=True, required=False)
    album = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(), allow_null=True, required=False)
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="name", required=False)
    mood = serializers.SlugRelatedField(
        queryset=Mood.objects.all(), slug_field="name", required=False)
    project_type = serializers.SlugRelatedField(
        queryset=ProjectType.objects.all(), slug_field="name", required=False)
    assigned_composer = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username", required=False)

    def validate(self, data):
        if len(data) == 1:  # Only track_ids provided
            raise serializers.ValidationError(
                "At least one field to update must be provided.")
        return data

    def create(self, validated_data):
        # This serializer is not meant to create new objects
        raise NotImplementedError(
            "BulkTrackUpdateSerializer does not support creation.")

    def update(self, instance, validated_data):
        track_ids = validated_data.pop('track_ids')
        Track.bulk_update_tracks(track_ids, **validated_data)
        return Track.objects.filter(id__in=track_ids)
