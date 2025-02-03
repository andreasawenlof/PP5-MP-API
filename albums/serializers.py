# pylint: disable=no-member

from instruments.models import Instrument
from rest_framework import serializers
from .models import Album
from tracks.models import Track, Genre, Mood, ProjectType


class SimpleTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title']


class DetailedTrackSerializer(serializers.ModelSerializer):

    instruments = serializers.SlugRelatedField(
        slug_field="name", read_only=True)

    class Meta:
        model = Track
        fields = [
            "id", "title", "album", "instruments",
            "status", "vocals_needed", "vocals_status", "assigned_composer",
            "notes", "created_at", "updated_at"]

# pylint: disable=no-member


# ... (keep SimpleTrackSerializer and DetailedTrackSerializer as they are)


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
        many=True, queryset=Track.objects.all(), required=False
    )

    class Meta:
        model = Album
        fields = [
            'id', 'title', 'owner', 'status', 'cover_art', 'notes',
            'project_type', 'genre', 'mood', 'created_at', 'updated_at', 'tracks', 'track_ids'
        ]

    def get_tracks(self, obj):
        tracks = obj.tracks.all()
        if self.context.get('is_detail', False):
            return DetailedTrackSerializer(tracks, many=True).data
        return SimpleTrackSerializer(tracks, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['track_ids'] = [
            track.id for track in instance.tracks.all()]
        return representation

    def create(self, validated_data):
        track_ids = validated_data.pop('track_ids', [])
        owner = self.context['request'].user
        album = Album.objects.create(owner=owner, **validated_data)

        for track in track_ids:
            album.tracks.add(track)
            track.album = album
            track.save()

        return album

    def update(self, instance, validated_data):
        track_ids = validated_data.pop('track_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if track_ids is not None:
            # Convert Track objects to IDs if necessary
            track_ids = [track.id if isinstance(
                track, Track) else track for track in track_ids]
            new_tracks = set(Track.objects.filter(id__in=track_ids))
            current_tracks = set(instance.tracks.all())

            tracks_to_remove = current_tracks - new_tracks
            for track in tracks_to_remove:
                instance.tracks.remove(track)
                track.album = None
                track.save()

            tracks_to_add = new_tracks - current_tracks
            for track in tracks_to_add:
                instance.tracks.add(track)
                track.album = instance
                track.save()

        # Update associated tracks with album's genre, mood, and project_type
        for track in instance.tracks.all():
            track.genre = instance.genre
            track.mood = instance.mood
            track.project_type = instance.project_type
            track.save()

        instance.save()
        return instance
