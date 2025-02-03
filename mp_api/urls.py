from django.contrib import admin
from django.urls import path, include
from tracks.views import (
    TrackListCreate, TrackDetail, MoodListCreate, GenreListCreate,
    ProjectTypeListCreate, BulkTrackUpdateView
)

urlpatterns = [
    # Admin & Authentication
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/auth/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/auth/dj-rest-auth/registration/',
         include('dj_rest_auth.registration.urls')),

    # ✅ API Endpoints
    path('api/tracks/', TrackListCreate.as_view(), name='track-list'),
    path('api/tracks/<int:pk>/', TrackDetail.as_view(), name='track-detail'),
    path('api/tracks/bulk-update/',
         BulkTrackUpdateView.as_view(), name='bulk-track-update'),
    path('api/moods/', MoodListCreate.as_view(), name='mood-list'),
    path('api/genres/', GenreListCreate.as_view(), name='genre-list'),
    path('api/project-types/', ProjectTypeListCreate.as_view(),
         name='project-type-list'),

    # ✅ Other Apps
    path('api/albums/', include('albums.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/instruments/', include('instruments.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/reviews/', include('reviews.urls')),
]
