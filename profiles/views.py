from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from mp_api.permissions import IsOwnerOrReadOnly, IsComposerOrOwner
from .serializers import ProfileSerializer
from .models import Profile


class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    # Only admins/editors can see the profile list
    permission_classes = [IsAuthenticated, IsComposerOrOwner]
    queryset = Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsComposerOrOwner, IsOwnerOrReadOnly]
    queryset = Profile.objects.all()

    def get_queryset(self):
        # Restrict to the logged-in user's profile
        return self.queryset.filter(owner=self.request.user)
