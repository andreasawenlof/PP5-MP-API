from rest_framework import generics
from tracks.models import Track
from .serializers import TrackSerializer
from django.http import JsonResponse


def home(request):
    return JsonResponse({"message": "Welcome to the MP_API!"})


class TrackListCreate(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
