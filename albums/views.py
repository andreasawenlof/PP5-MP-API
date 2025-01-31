from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Album
from .serializers import AlbumSerializer


class AlbumList(generics.ListCreateAPIView):
    serializer_class = AlbumSerializer
    permission_class = [IsAuthenticated]
    queryset = Album.objects.all()


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumSerializer
    permission_class = [IsAuthenticated]
    queryset = Album.objects.all()
