from .serializers import InstrumentSerializer, InstrumentCategorySerializer
from rest_framework import generics
from .models import InstrumentCategory, Instrument
from mp_api.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated


class InstrumentCategoryList(generics.ListCreateAPIView):
    queryset = InstrumentCategory.objects.all()
    serializer_class = InstrumentCategorySerializer
    permission_classes = [IsAuthenticated]


class InstrumentList(generics.ListCreateAPIView):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    permission_classes = [IsAuthenticated]


class InstrumentCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InstrumentCategory.objects.all()
    serializer_class = InstrumentCategorySerializer
    permission_classes = [IsAuthenticated]


class InstrumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    permission_classes = [IsOwnerOrReadOnly]
