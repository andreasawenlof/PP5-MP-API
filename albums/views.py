from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Album
from .serializers import AlbumSerializer
from mp_api.permissions import IsComposerOrOwner


class AlbumListCreate(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]

    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['status', 'genre', 'mood', 'project_type']
    ordering_fields = ['created_at', 'updated_at', 'title']
    search_fields = ['title', 'notes']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['is_detail'] = False
        return context


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['is_detail'] = True
        return context
