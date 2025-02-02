from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Album
from .serializers import AlbumSerializer


class AlbumListCreate(generics.ListCreateAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]
    queryset = Album.objects.all()


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]
    queryset = Album.objects.all()
