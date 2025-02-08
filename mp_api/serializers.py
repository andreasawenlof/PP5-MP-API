from rest_framework import serializers
from tracks.models import Track, Genre, Mood, ProjectType, Album, User


class UserSerializer(serializers.ModelSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.avatar.url')
    display_name = serializers.ReadOnlyField(source='profile.display_name')
    is_composer = serializers.ReadOnlyField(source='profile.is_composer')
    is_reviewer = serializers.ReadOnlyField(source='profile.is_reviewer')

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_id', 'display_name',
                  'profile_image', 'is_composer', 'is_reviewer', 'profile_image']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ['id', 'name']


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ['id', 'name']


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name']


class TrackSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    mood = MoodSerializer(read_only=True)
    project_type = ProjectTypeSerializer(read_only=True)
    album = AlbumSerializer(read_only=True)
    assigned_composer = UserSerializer(
        read_only=True)

    class Meta:
        model = Track
        fields = [
            'id', 'title', 'notes', 'status', 'vocals_needed', 'vocals_status',
            'project_type', 'genre', 'mood', 'album', 'assigned_composer',
            'created_at', 'updated_at'
        ]
