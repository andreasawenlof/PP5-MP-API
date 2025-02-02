from rest_framework import serializers
from .models import Album
from tracks.models import Track, Genre, Mood, ProjectType


class AlbumSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="name", required=False
    )
    mood = serializers.SlugRelatedField(
        queryset=Mood.objects.all(), slug_field="name", required=False
    )
    project_type = serializers.SlugRelatedField(
        queryset=ProjectType.objects.all(), slug_field="name", required=False
    )
    tracks = serializers.SlugRelatedField(
        queryset=Track.objects.all(), slug_field="title", many=True, required=False
    )

    class Meta:
        model = Album
        fields = "__all__"
