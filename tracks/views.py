from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Track
from .serializers import TrackSerializer


class TrackList(generics.ListCreateAPIView):
    serializer_class = TrackSerializer
    permission_class = [IsAuthenticated]
    queryset = Track.objects.all()


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrackSerializer
    permission_class = [IsAuthenticated]
    queryset = Track.objects.all()
