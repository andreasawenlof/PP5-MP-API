from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Track, Mood, Genre, ProjectType
from .serializers import TrackSerializer, MoodSerializer, GenreSerializer, ProjectTypeSerializer, BulkTrackUpdateSerializer
from mp_api.permissions import IsComposerOrOwner, IsReviewer
import logging

logger = logging.getLogger(__name__)


class TrackViewSet(viewsets.ModelViewSet):
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profile.is_composer:
            return Track.objects.all()
        if user.profile.is_reviewer:
            return Track.objects.filter(status="ready_for_review")
        return Track.objects.none()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsComposerOrOwner]
        elif self.action == "list":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logger.info(f"Retrieving track data: {serializer.data}")
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating track with data: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info(f"Updated track data: {serializer.data}")
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class MoodViewSet(viewsets.ModelViewSet):
    serializer_class = MoodSerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]
    queryset = Mood.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]
    queryset = Genre.objects.all()


class ProjectTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectTypeSerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]
    queryset = ProjectType.objects.all()


class BulkTrackUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsComposerOrOwner]

    def patch(self, request, *args, **kwargs):
        serializer = BulkTrackUpdateSerializer(data=request.data)
        if serializer.is_valid():
            updated_tracks = serializer.update(None, serializer.validated_data)
            return Response(TrackSerializer(updated_tracks, many=True).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
