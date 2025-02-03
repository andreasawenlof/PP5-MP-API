# pylint: disable=no-member

from rest_framework import serializers
from django.db import transaction
from .models import Album
from tracks.models import Track, Genre, Mood, ProjectType


class SimpleTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title']


class DetailedTrackSerializer(serializers.ModelSerializer):
    instruments = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=True
    )

    class Meta:
        model = Track
        fields = [
            "id", "title", "album", "instruments",
            "status", "vocals_needed", "vocals_status", "assigned_composer",
            "notes", "created_at", "updated_at"
        ]


class AlbumSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="name", required=False, allow_null=True
    )
    mood = serializers.SlugRelatedField(
        queryset=Mood.objects.all(), slug_field="name", required=False, allow_null=True
    )
    project_type = serializers.SlugRelatedField(
        queryset=ProjectType.objects.all(), slug_field="name", required=False, allow_null=True
    )
    tracks = serializers.SerializerMethodField()
    track_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Track.objects.all(), required=False, write_only=True
    )

    class Meta:
        model = Album
        fields = [
            'id', 'title', 'owner', 'status', 'cover_art', 'notes',
            'project_type', 'genre', 'mood', 'created_at', 'updated_at', 'tracks', 'track_ids'
        ]

    def get_tracks(self, obj):
        tracks = obj.tracks.all()
        serializer = DetailedTrackSerializer if self.context.get(
            'is_detail', False) else SimpleTrackSerializer
        return serializer(tracks, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['track_ids'] = list(
            instance.tracks.values_list('id', flat=True))
        return representation

    @transaction.atomic
    def create(self, validated_data):
        track_ids = validated_data.pop('track_ids', [])
        owner = self.context['request'].user
        album = Album.objects.create(owner=owner, **validated_data)
        self._update_tracks(album, track_ids)
        return album

    @transaction.atomic
    def update(self, instance, validated_data):
        track_ids = validated_data.pop('track_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if track_ids is not None:
            self._update_tracks(instance, track_ids)

        return instance

    def _update_tracks(self, album, track_ids):
        current_tracks = set(album.tracks.all())
        new_tracks = set(Track.objects.filter(id__in=track_ids))

        tracks_to_remove = current_tracks - new_tracks
        tracks_to_add = new_tracks - current_tracks

        album.tracks.remove(*tracks_to_remove)
        album.tracks.add(*tracks_to_add)

        Track.objects.filter(
            id__in=[t.id for t in tracks_to_remove]).update(album=None)
        Track.objects.filter(id__in=[t.id for t in tracks_to_add]).update(
            album=album,
            genre=album.genre,
            mood=album.mood,
            project_type=album.project_type
        )
