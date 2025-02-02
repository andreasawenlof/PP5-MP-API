from django.urls import path
from .views import (
    TrackListCreate,
    TrackDetail,
    MoodListCreate,
    GenreListCreate,
    ProjectTypeListCreate,
    MoodDetail,
    GenreDetail,
    ProjectTypeDetail,
)

urlpatterns = [
    path("", TrackListCreate.as_view(), name="track-list"),
    path("<int:pk>/", TrackDetail.as_view(), name="track-detail"),

]
