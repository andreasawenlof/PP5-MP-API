from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from mp_api.permissions import IsOwnerOrReadOnly
from .serializers import ProfileSerializer
from .models import Profile
from rest_framework.exceptions import PermissionDenied


class ProfileList(generics.ListAPIView):
    """✅ All authenticated users can view all profiles."""
    serializer_class = ProfileSerializer
    # ✅ Only logged-in users can see profiles
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """✅ All users can view profiles, but ONLY owners can edit their own."""
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """✅ Authenticated users can see all profiles."""
        return Profile.objects.all()  # ✅ Any logged-in user can see profiles

    def perform_update(self, serializer):
        """✅ Only the profile owner can edit their own profile."""
        if self.request.user != serializer.instance.owner:
            raise PermissionDenied("You can only edit your own profile.")
        serializer.save()
