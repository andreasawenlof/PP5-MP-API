from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracks.views import TrackViewSet, MoodViewSet, GenreViewSet, ProjectTypeViewSet, BulkTrackUpdateView

# ✅ Register ViewSets for Auto-Generated Endpoints
router = DefaultRouter()
router.register(r'tracks', TrackViewSet, basename="tracks")
router.register(r'moods', MoodViewSet, basename="moods")
router.register(r'genres', GenreViewSet, basename="genres")
router.register(r'project-types', ProjectTypeViewSet, basename="project-types")

urlpatterns = [
    # Admin & Authentication
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/auth/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/auth/dj-rest-auth/registration/',
         include('dj_rest_auth.registration.urls')),

    # ✅ Main API Endpoints
    # 🔥 Now moods, genres, and project-types are handled automatically
    path('api/', include(router.urls)),
    path('api/albums/', include('albums.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/instruments/', include('instruments.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/reviews/', include('reviews.urls')),

    # ✅ Bulk Update Stays as a Separate Path
    path("api/tracks/bulk-update/",
         BulkTrackUpdateView.as_view(), name="bulk-track-update"),
]
