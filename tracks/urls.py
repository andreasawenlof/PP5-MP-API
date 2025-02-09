from django.urls import path
from .views import (
    TrackListCreate,
    TrackDetail,
    MoodListCreate,
    GenreListCreate,
    ProjectTypeListCreate,
    BulkTrackUpdateView,
)

urlpatterns = [
    path("tracks/", TrackListCreate.as_view(), name="track-list"),
    path("tracks/<int:pk>/", TrackDetail.as_view(), name="track-detail"),
    path(
        "tracks/bulk-update/", BulkTrackUpdateView.as_view(), name="bulk-track-update"
    ),
    path("moods/", MoodListCreate.as_view(), name="mood-list"),
    path("genres/", GenreListCreate.as_view(), name="genre-list"),
    path("project-types/", ProjectTypeListCreate.as_view(), name="project-type-list"),
]
