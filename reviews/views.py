from rest_framework import generics
from .models import Review, ReviewHistory
from .serializers import ReviewSerializer, ReviewHistorySerializer
from rest_framework.permissions import IsAuthenticated
from mp_api.permissions import IsOwnerOrReadOnly, IsEditorOrOwner


class ReviewListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Editors see all reviews.
        Reviewers see only their assigned reviews.
        """
        user = self.request.user
        if user.profile.is_editor:
            return Review.objects.all()
        return Review.objects.filter(reviewer=user)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Editors see all reviews.
        Reviewers see only their assigned reviews.
        """
        user = self.request.user
        if user.profile.is_editor:
            return Review.objects.all()
        return Review.objects.filter(reviewer=user)


class ReviewHistoryListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewHistorySerializer
    permission_classes = [IsAuthenticated, IsEditorOrOwner]

    def get_queryset(self):
        """
        Editors see all review history.
        Reviewers see only history related to their reviews.
        """
        user = self.request.user
        if user.profile.is_editor:
            return ReviewHistory.objects.all()
        return ReviewHistory.objects.filter(review__reviewer=user)

    def perform_create(self, serializer):
        serializer.save(editor=self.request.user)


class ReviewHistoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewHistorySerializer
    permission_classes = [IsAuthenticated, IsEditorOrOwner]

    def get_queryset(self):
        """
        Editors see all review history.
        Reviewers see only history related to their reviews.
        """
        user = self.request.user
        if user.profile.is_editor:
            return ReviewHistory.objects.all()
        return ReviewHistory.objects.filter(review__reviewer=user)
