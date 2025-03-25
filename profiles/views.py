from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from mp_api.permissions import IsComposerOrOwner
from .serializers import ProfileSerializer
from .models import Profile
from django.http import Http404


class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsComposerOrOwner]

    queryset = Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    queryset = Profile.objects.all()

    def get_object(self):
        profile = super().get_object()
        user = self.request.user

        # ✅ Composers can view any profile
        if user.profile.is_composer:
            return profile

        # ✅ Owners can view their own profile
        if profile.owner == user:
            return profile

        # ❌ Everyone else gets a 404
        raise Http404("Profile not found.")

    def perform_update(self, serializer):
        """✅ Only the profile owner can edit their own profile."""
        if self.request.user != serializer.instance.owner:
            raise PermissionDenied("You can only edit your own profile.")
        serializer.save()
