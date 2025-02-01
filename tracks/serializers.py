from rest_framework import serializers
from .models import Track, Instrument
from albums.models import Album
from django.contrib.auth.models import User


class TrackSerializer(serializers.ModelSerializer):
    # album = serializers.ReadOnlyField(source='album.title')
    album = serializers.SerializerMethodField()
    instruments = serializers.CharField(source='instruments.name')
    # instruments = serializers.PrimaryKeyRelatedField(
    #     queryset=Instrument.objects.all(), many=True, required=False
    # )
    assigned_user = serializers.ReadOnlyField(source='assigned_user.username')

    class Meta:
        model = Track
        fields = '__all__'
