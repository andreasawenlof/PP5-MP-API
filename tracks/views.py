from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Track, Genre, Mood, ProjectType
from .serializers import (
    TrackSerializer,
    MoodSerializer,
    GenreSerializer,
    ProjectTypeSerializer,
)


class TrackListCreate(generics.ListCreateAPIView):
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]
    queryset = Track.objects.all()

    def perform_create(self, serializer):
        serializer.save(assigned_user=self.request.user)


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]
    queryset = Track.objects.all()


# Separate views to create & list moods, genres, project types
class MoodListCreate(generics.ListCreateAPIView):
    serializer_class = MoodSerializer
    permission_classes = [IsAuthenticated]
    queryset = Mood.objects.all()


class MoodDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MoodSerializer
    permission_classes = [IsAuthenticated]
    queryset = Mood.objects.all()


class GenreListCreate(generics.ListCreateAPIView):
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]
    queryset = Genre.objects.all()


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]
    queryset = Genre.objects.all()


class ProjectTypeListCreate(generics.ListCreateAPIView):
    serializer_class = ProjectTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = ProjectType.objects.all()


class ProjectTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = ProjectType.objects.all()
