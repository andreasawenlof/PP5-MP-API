from rest_framework import serializers
from .models import Comment
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username"
    )
    profile_image = serializers.CharField(
        source='author.profile.avatar.url', read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'profile_image', 'track', 'album',
            'created_at', 'updated_at'
        ]
