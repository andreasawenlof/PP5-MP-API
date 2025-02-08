from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Track, Mood, Genre, ProjectType
from .serializers import TrackSerializer, MoodSerializer, GenreSerializer, ProjectTypeSerializer, BulkTrackUpdateSerializer
from mp_api.permissions import IsComposerOrOwner, IsReviewer, IsComposerOrReviewer, IsOwnerOrReadOnly


class TrackListCreate(generics.ListCreateAPIView):
    """
    - Composers: See all tracks & create new ones.
    - Reviewers: See only 'ready_for_review' tracks, NO CREATE PERMISSION.
    - Normal users: See nothing.
    """
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated, IsComposerOrReviewer]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = {
        "assigned_composer": ["exact"],  # Filter by assigned composer
        "project_type": ["exact"],  # Filter by project type
        "genre": ["exact"],  # Filter by genre
        "mood": ["exact"],  # Filter by mood
        "instruments": ["exact"],  # Filter by instruments
        "vocals_needed": ["exact"],  # Filter by whether vocals are needed
        "status": ["exact"],  # Filter by track status
    }

    # Search by track title & album name
    search_fields = ["title", "album__title"]
    ordering_fields = ["created_at", "updated_at", "title"]  # Sorting options
    ordering = ["-updated_at"]  # Default order is newest updated

    def get_queryset(self):
        user = self.request.user
        if user.profile.is_composer:
            return Track.objects.all()
        if user.profile.is_reviewer:
            return Track.objects.filter(status="ready_for_review")
        return Track.objects.none()

    def perform_create(self, serializer):
        if not self.request.user.profile.is_composer:
            raise NotFound()  # ✅ Only composers can create tracks

        # Default to the logged-in user as the assigned_composer
        assigned_composer = self.request.user

        # Allow manual override if a composer is explicitly chosen
        if serializer.validated_data.get('assigned_composer'):
            assigned_composer = serializer.validated_data['assigned_composer']

        # Save the track with the assigned composer and owner
        serializer.save(owner=self.request.user,
                        assigned_composer=assigned_composer)


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    - Composers: Can view, update, and delete.
    - Reviewers: Can ONLY view 'ready_for_review' tracks (NO EDIT/DELETE).
    """
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated, IsComposerOrReviewer]

    def get_object(self):
        """
        ✅ Ensures reviewers NEVER see tracks they shouldn’t.
        ✅ NO MORE 403 Forbidden – Reviewers get clean 404 (Not Found).
        """
        user = self.request.user
        track_id = self.kwargs["pk"]

        try:
            obj = Track.objects.get(pk=track_id)
        except Track.DoesNotExist:
            raise NotFound()

        # ✅ Composers can see everything
        if user.profile.is_composer:
            return obj

        # ✅ Reviewers can ONLY see 'ready_for_review' tracks
        if user.profile.is_reviewer and obj.status == "ready_for_review":
            return obj

        raise NotFound()  # ✅ Acts like the track never existed (NO 403!)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.profile.is_reviewer:
            raise NotFound()  # ✅ Reviewers CANNOT edit
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.profile.is_reviewer:
            raise NotFound()  # ✅ Reviewers CANNOT delete
        return super().destroy(request, *args, **kwargs)


# ✅ MOODS
class MoodListCreate(generics.ListCreateAPIView):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]


# ✅ GENRES
class GenreListCreate(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]


# ✅ PROJECT TYPES
class ProjectTypeListCreate(generics.ListCreateAPIView):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]


# ✅ BULK UPDATES
class BulkTrackUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsComposerOrOwner]
    serializer_class = BulkTrackUpdateSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_tracks = serializer.update(None, serializer.validated_data)
        return Response(TrackSerializer(updated_tracks, many=True).data)
