from rest_framework.exceptions import NotFound
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from mp_api.permissions import IsOwnerOrReadOnly, IsComposerOrOwner
from rest_framework import serializers


class CommentList(generics.ListCreateAPIView):
    """
    List all comments or create a new comment.
    - ✅ Any authenticated user can view/create comments (for now).
    - 🔒 Role logic is DISABLED but kept for later.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]

    def get_queryset(self):
        """✅ Return only comments for a specific track or album."""
        user = self.request.user
        track_id = self.request.query_params.get("track")
        album_id = self.request.query_params.get("album")

        if not track_id and not album_id:
            return Comment.objects.none()  # ✅ No track/album = No comments

        queryset = Comment.objects.select_related("owner", "track", "album")

        # ✅ Filter by track or album
        if track_id:
            queryset = queryset.filter(track_id=track_id)
        elif album_id:
            queryset = queryset.filter(album_id=album_id)

        return queryset

    def perform_create(self, serializer):
        """✅ Any authenticated user can create comments (for now)."""
        user = self.request.user
        # 🔒 Keep the role logic but disable it for submission
        # if not user.profile.is_composer:
        #     raise NotFound()  # ✅ Pretend the feature doesn’t exist
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve comment details.
    - ✅ Any authenticated user can view comments (for now).
    - ✅ Only owners can edit/delete their own comments.
    - 🔒 Role logic is DISABLED but kept for later.
    """

    queryset = Comment.objects.select_related("owner", "track", "album")
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        """
        ✅ Only owners can edit/delete their comments.
        🔒 Reviewers & Unauthorized Users logic is DISABLED for now.
        """
        user = self.request.user
        comment_id = self.kwargs["pk"]

        try:
            obj = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise NotFound()

        # 🔒 Keep the role logic but disable it for submission
        # if not user.profile.is_composer and obj.owner != user:
        #     raise NotFound()  # ✅ Reviewers & Unauthorized Users see NOTHING

        return obj

    def perform_update(self, serializer):
        """
        Make sure a track or album is associated when updating a comment.
        """
        track = self.request.data.get("track")
        album = self.request.data.get("album")

        if not track and not album:
            raise serializers.ValidationError(
                "A comment must be associated with either a track or an album."
            )

        # ✅ Finally save the updated data!
        serializer.save()
