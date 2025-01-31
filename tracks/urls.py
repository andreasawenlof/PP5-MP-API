from django.urls import path
from .views import TrackList, TrackDetail

urlpatterns = [
    path('', TrackList.as_view(), name='track-list'),
    path('<int:pk>/', TrackDetail.as_view(), name='track-detail'),
]
