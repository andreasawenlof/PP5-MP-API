from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    profile_image = serializers.CharField(
        source='author.profile.avatar.url', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'track', 'album',
                  'created_at', 'updated_at', 'profile_image']
