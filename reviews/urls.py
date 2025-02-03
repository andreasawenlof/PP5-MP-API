from django.urls import path
from .views import ReviewListCreate, ReviewDetail, ReviewHistoryListCreate, ReviewHistoryDetail

urlpatterns = [
    path('', ReviewListCreate.as_view(), name='review-list'),
    path('<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('history/', ReviewHistoryListCreate.as_view(),
         name='review-history-list'),
    path('history/<int:pk>/', ReviewHistoryDetail.as_view(),
         name='review-history-detail'),
]
