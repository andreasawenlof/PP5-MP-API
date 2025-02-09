from rest_framework import generics
from .models import Review, ReviewHistory
from .serializers import ReviewSerializer, ReviewHistorySerializer
from rest_framework.permissions import IsAuthenticated
from mp_api.permissions import IsOwnerOrReadOnly, IsComposerOrOwner


class ReviewListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """- Reviewers see all reviews for 'ready_for_review' tracks.
        - Composers see everything."""
        user = self.request.user
        if user.profile.is_composer:
            return Review.objects.all()
        return Review.objects.filter(track__status="ready_for_review")

    def perform_create(self, serializer):
        """🔹 If review exists for track, append to history instead of creating a new one."""
        track = serializer.validated_data["track"]
        existing_review = Review.objects.filter(track=track).first()

        if existing_review:
            # Append new feedback to history instead of creating a new review
            ReviewHistory.objects.create(
                review=existing_review,
                editor=self.request.user,
                updated_feedback=serializer.validated_data["feedback"],
                revision_number=existing_review.history.count() + 1,
            )
            return  # Prevents new review creation

        # If no review exists, create a new one
        serializer.save(reviewer=self.request.user)


class ReviewDetail(generics.RetrieveAPIView):  # ✅ Read-Only View
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        - Reviewers see only their reviews for 'ready_for_review' tracks.
        - Composers see everything.
        """
        user = self.request.user
        if user.profile.is_composer:
            return Review.objects.all()
        return Review.objects.filter(track__status="ready_for_review", reviewer=user)


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
        return ReviewHistory.objects.filter(
            review__track__status="ready_for_review", review__reviewer=user
        )

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
        return ReviewHistory.objects.filter(
            review__track__status="ready_for_review", review__reviewer=user
        )
