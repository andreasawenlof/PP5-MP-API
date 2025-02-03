from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from mp_api.permissions import IsOwnerOrReadOnly, IsComposerOrOwner


class CommentList(generics.ListCreateAPIView):
    """
    List all comments or create a new comment.
    - Only authenticated composers/owners can create/view comments.
    - Filters comments by track or album.
    - Optimized with select_related to reduce database queries.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]

    def get_queryset(self):
        """Filter comments by track or album if provided."""
        queryset = Comment.objects.select_related("owner", "track", "album")
        track = self.request.query_params.get("track")
        album = self.request.query_params.get("album")

        if track:
            queryset = queryset.filter(track__id=track)
        elif album:
            queryset = queryset.filter(album__id=album)

        return queryset

    def perform_create(self, serializer):
        """Assign the logged-in user as the comment owner."""
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a comment.
    - Only the owner can update or delete their own comment.
    - Optimized with select_related to reduce database queries.
    """
    queryset = Comment.objects.select_related("owner", "track", "album")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
