from django.urls import path
from .views import CommentList, CommentDetail

urlpatterns = [
    path('', CommentList.as_view(), name='comments-list'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
]
