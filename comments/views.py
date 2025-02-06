from rest_framework.exceptions import NotFound
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from mp_api.permissions import IsOwnerOrReadOnly, IsComposerOrOwner


class CommentList(generics.ListCreateAPIView):
    """
    List all comments or create a new comment.
    - Only authenticated composers/owners can create/view comments.
    - Reviewers & Unauthorized Users see NOTHING (no comments, no form, no errors).
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """✅ Reviewers & Unauthorized Users see NOTHING (Empty List)."""
        user = self.request.user
        if user.profile.is_composer:
            return Comment.objects.select_related("owner", "track", "album")
        return Comment.objects.none()  # ✅ Just return an empty list for them

    def perform_create(self, serializer):
        """✅ Only composers can create comments. Reviewers see NOTHING."""
        user = self.request.user
        if not user.profile.is_composer:
            raise NotFound()  # ✅ Pretend the feature doesn’t exist
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveAPIView):
    """
    Retrieve comment details.
    - ✅ Only composers & owners can view comments.
    - ❌ Reviewers & unauthorized users see NOTHING (404).
    """
    queryset = Comment.objects.select_related("owner", "track", "album")
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        """
        ✅ Reviewers & Unauthorized Users get a 404.
        ✅ Only composers & owners can access comments.
        """
        user = self.request.user
        comment_id = self.kwargs["pk"]

        try:
            obj = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise NotFound()

        # ✅ Composers & Owners can access everything
        if user.profile.is_composer or obj.owner == user:
            return obj

        raise NotFound()  # ✅ Reviewers & Unauthorized Users see NOTHING
