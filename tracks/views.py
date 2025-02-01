from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Track
from .serializers import TrackSerializer


class TrackList(generics.ListCreateAPIView):
    serializer_class = TrackSerializer
    permission_class = [IsAuthenticated]
    queryset = Track.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrackSerializer
    permission_class = [IsAuthenticated]
    queryset = Track.objects.all()
