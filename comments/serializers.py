from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.CharField(
        source='owner.profile.avatar.url', read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'profile_id', 'profile_image', 'track', 'album', 'content',
            'created_at', 'updated_at'
        ]

    def validate(self, data):
        track = data.get('track')
        album = data.get('album')

        if track and album:
            raise serializers.ValidationError(
                "A comment can only be associated with either a track or an album, not both.")
        if not track and not album:
            raise serializers.ValidationError(
                "A comment must be associated with either a track or an album.")

        return data
