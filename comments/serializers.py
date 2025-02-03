from rest_framework import serializers
from .models import Comment
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.CharField(
        source='owner.profile.avatar.url', read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'profile_id', 'profile_image', 'track', 'album',
            'created_at', 'updated_at'
        ]
