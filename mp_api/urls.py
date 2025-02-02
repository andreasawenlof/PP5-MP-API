"""
URL configuration for mp_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tracks.views import (
    MoodListCreate, MoodDetail,
    GenreListCreate, GenreDetail,
    ProjectTypeListCreate, ProjectTypeDetail)

urlpatterns = [
    # Admin & Authentication
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/auth/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/auth/dj-rest-auth/registration/',
         include('dj_rest_auth.registration.urls')),

    # Main API Endpoints
    path('api/tracks/', include('tracks.urls')),
    path('api/albums/', include('albums.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/instruments/', include('instruments.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/reviews/', include('reviews.urls')),

    # ✅ Moods, Genres, and Project Types - Kept in Main URLs
    path("api/moods/", MoodListCreate.as_view(), name="mood-list"),
    path("api/moods/<int:pk>/", MoodDetail.as_view(), name="mood-detail"),
    path("api/genres/", GenreListCreate.as_view(), name="genre-list"),
    path("api/genres/<int:pk>/", GenreDetail.as_view(), name="genre-detail"),
    path("api/project-types/", ProjectTypeListCreate.as_view(),
         name="project-type-list"),
    path("api/project-types/<int:pk>/",
         ProjectTypeDetail.as_view(), name="project-type-detail"),
]
