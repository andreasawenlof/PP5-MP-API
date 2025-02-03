from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
# If you want to restrict updates to the owner only
from mp_api.permissions import IsOwnerOrReadOnly, IsComposerOrOwner


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # Only authenticated users can add/view comments
    permission_classes = [IsAuthenticated, IsComposerOrOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # Only owner can edit or delete
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
