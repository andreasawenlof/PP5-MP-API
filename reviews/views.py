from rest_framework import generics
from .models import Review, ReviewHistory
from .serializers import ReviewSerializer, ReviewHistorySerializer
from rest_framework.permissions import IsAuthenticated
from mp_api.permissions import IsOwnerOrReadOnly, IsComposerOrOwner


class ReviewListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        - Reviewers see all reviews for 'ready_for_review' tracks.
        - Composers see everything.
        """
        user = self.request.user
        if user.profile.is_composer:
            return Review.objects.all()
        return Review.objects.filter(track__status="ready_for_review")

    def perform_create(self, serializer):
        """
        - Assigns reviewer as the logged-in user.
        - Makes sure review is locked after submission.
        """
        serializer.save(reviewer=self.request.user)


class ReviewDetail(generics.RetrieveAPIView):  # ✅ Read-Only View
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        - Reviewers see all reviews for 'ready_for_review' tracks.
        - Composers see everything.
        """
        user = self.request.user
        if user.profile.is_composer:
            return Review.objects.all()
        return Review.objects.filter(track__status="ready_for_review")


class ReviewHistoryListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewHistorySerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]

    def get_queryset(self):
        """
        - Reviewers and composers can see review history for 'ready_for_review' tracks.
        - Only composers see the revision count.
        """
        user = self.request.user
        if user.profile.is_composer:
            return ReviewHistory.objects.all()
        return ReviewHistory.objects.filter(review__track__status="ready_for_review")

    def perform_create(self, serializer):
        serializer.save(editor=self.request.user)


class ReviewHistoryDetail(generics.RetrieveAPIView):  # ✅ Read-Only View
    serializer_class = ReviewHistorySerializer
    permission_classes = [IsAuthenticated, IsComposerOrOwner]

    def get_queryset(self):
        """
        - Reviewers and composers can see review history for 'ready_for_review' tracks.
        - Only composers see the revision count.
        """
        user = self.request.user
        if user.profile.is_composer:
            return ReviewHistory.objects.all()
        return ReviewHistory.objects.filter(review__track__status="ready_for_review")
