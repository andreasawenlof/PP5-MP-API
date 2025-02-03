from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment
from tracks.models import Track
from albums.models import Album
from profiles.models import Profile


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Handles serialization and deserialization of Comment objects.
    """
    owner = serializers.ReadOnlyField(source='owner.profile.display_name')
    profile_image = serializers.CharField(
        source='owner.profile.avatar.url', read_only=True
    )
    is_composer = serializers.BooleanField(
        source='owner.profile.is_composer', read_only=True
    )
    is_reviewer = serializers.BooleanField(
        source='owner.profile.is_reviewer', read_only=True
    )

    track = serializers.SlugRelatedField(
        queryset=Track.objects.all(),
        slug_field='title',
        required=False,
        allow_null=True
    )
    album = serializers.SlugRelatedField(
        queryset=Album.objects.all(),
        slug_field='title',
        required=False,
        allow_null=True
    )
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'profile_image', 'track', 'album', 'content', 'is_composer', 'is_reviewer',
            'created_at', 'updated_at'
        ]

    def validate(self, data):
        """
        Validate that a comment is associated with either a track or an album, but not both.
        """
        track = data.get('track')
        album = data.get('album')

        if track and album:
            raise serializers.ValidationError(
                "A comment can only be associated with either a track or an album, not both.")
        if not track and not album:
            raise serializers.ValidationError(
                "A comment must be associated with either a track or an album.")

        return data
