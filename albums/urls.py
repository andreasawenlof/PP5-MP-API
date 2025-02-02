from django.urls import path
from .views import AlbumListCreate, AlbumDetail

urlpatterns = [
    path('', AlbumListCreate.as_view(), name='album-list'),
    path('<int:pk>/', AlbumDetail.as_view(), name='album-detail'),
]
