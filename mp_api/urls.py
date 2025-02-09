from django.contrib import admin
from django.urls import path, include
from tracks.views import (
    TrackListCreate,
    TrackDetail,
    MoodListCreate,
    GenreListCreate,
    ProjectTypeListCreate,
    BulkTrackUpdateView,
)
from .views import home
from mp_api.auth_views import CustomLogoutView  # Import your custom logout view
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.http import JsonResponse
from django.middleware.csrf import get_token


def csrf_token_view(request):
    return JsonResponse({"csrfToken": get_token(request)})


urlpatterns = [
    # Admin & Authentication
    path("admin/", admin.site.urls),
    path("dj-rest-auth/logout/", CustomLogoutView.as_view(), name="rest_logout"),
    path("api/auth/", include("rest_framework.urls")),
    # Place the custom logout view BEFORE including dj-rest-auth URLs
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "dj-rest-auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("dj-rest-auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("csrf/", csrf_token_view, name="csrf"),
    # ✅ API Endpoints
    path("", home, name="home"),
    path("api/tracks/", TrackListCreate.as_view(), name="track-list"),
    path("api/tracks/<int:pk>/", TrackDetail.as_view(), name="track-detail"),
    path(
        "api/tracks/bulk-update/",
        BulkTrackUpdateView.as_view(),
        name="bulk-track-update",
    ),
    path("api/moods/", MoodListCreate.as_view(), name="mood-list"),
    path("api/genres/", GenreListCreate.as_view(), name="genre-list"),
    path(
        "api/project-types/", ProjectTypeListCreate.as_view(), name="project-type-list"
    ),
    # ✅ Other Apps
    path("api/albums/", include("albums.urls")),
    path("api/profiles/", include("profiles.urls")),
    path("api/instruments/", include("instruments.urls")),
    path("api/comments/", include("comments.urls")),
    path("api/reviews/", include("reviews.urls")),
]
