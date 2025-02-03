from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    TrackViewSet, MoodViewSet, GenreViewSet, ProjectTypeViewSet, BulkTrackUpdateView
)

# DRF Router for standard CRUD views
router = DefaultRouter()
router.register(r'tracks', TrackViewSet, basename="tracks")
router.register(r'moods', MoodViewSet, basename="moods")
router.register(r'genres', GenreViewSet, basename="genres")
router.register(r'project-types', ProjectTypeViewSet, basename="project-types")

# Custom path for bulk updates
urlpatterns = router.urls + [
    path("tracks/bulk-update/", BulkTrackUpdateView.as_view(),
         name="bulk-track-update"),
]
