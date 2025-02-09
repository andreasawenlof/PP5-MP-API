from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import InstrumentSerializer, InstrumentCategorySerializer
from rest_framework import generics
from .models import InstrumentCategory, Instrument
from mp_api.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound


class InstrumentCategoryList(generics.ListCreateAPIView):
    """
    ✅ Composers can create/list instrument categories.
    ✅ Reviewers/unauthorized users see NOTHING.
    """

    serializer_class = InstrumentCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """✅ Only composers can see instrument categories, others get 404."""
        user = self.request.user
        if user.profile.is_composer:
            return InstrumentCategory.objects.all()
        raise NotFound()

    def perform_create(self, serializer):
        """✅ Only composers can create instrument categories."""
        if not self.request.user.profile.is_composer:
            raise NotFound()
        serializer.save()


class InstrumentList(generics.ListCreateAPIView):
    """
    ✅ Composers can create/list instruments.
    ✅ Reviewers/unauthorized users see NOTHING.
    ✅ Filtering & search enabled for composers.
    """

    serializer_class = InstrumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["categories"]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        """✅ Only composers can see instruments, others get 404."""
        user = self.request.user
        if user.profile.is_composer:
            return Instrument.objects.all()
        raise NotFound()

    def perform_create(self, serializer):
        """✅ Only composers can create instruments."""
        if not self.request.user.profile.is_composer:
            raise NotFound()
        serializer.save()


class InstrumentCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ Composers can view/edit/delete instrument categories.
    ✅ Reviewers/unauthorized users get a 404.
    """

    serializer_class = InstrumentCategorySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """✅ Only composers can see instrument categories, others get 404."""
        user = self.request.user
        if user.profile.is_composer:
            return InstrumentCategory.objects.all()
        raise NotFound()


class InstrumentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ Composers can view/edit/delete instruments.
    ✅ Reviewers/unauthorized users get a 404.
    """

    serializer_class = InstrumentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """✅ Only composers can see instruments, others get a 404."""
        user = self.request.user
        if user.profile.is_composer:
            return Instrument.objects.all()
        raise NotFound()
