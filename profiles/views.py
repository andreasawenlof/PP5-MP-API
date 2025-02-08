from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from mp_api.permissions import IsComposerOrOwner
from .serializers import ProfileSerializer
from .models import Profile


class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsComposerOrOwner]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsComposerOrOwner]

    def perform_update(self, serializer):
        """✅ Only the profile owner can edit their own profile."""
        if self.request.user != serializer.instance.owner:
            raise PermissionDenied("You can only edit your own profile.")
        serializer.save()
