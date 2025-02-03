from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import QuerySet
from .models import Album
from .serializers import AlbumSerializer
from mp_api.permissions import IsComposerOrOwner


class AlbumListCreate(generics.ListCreateAPIView):
    queryset: QuerySet[Album] = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['is_detail'] = False
        return context


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset: QuerySet[Album] = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['is_detail'] = True
        return context
