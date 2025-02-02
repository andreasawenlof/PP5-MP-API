from django.urls import path
from .views import InstrumentList, InstrumentDetail, InstrumentCategoryList, InstrumentCategoryDetail

urlpatterns = [
    path('', InstrumentList.as_view(), name='instrument-list'),
    path('<int:pk>/', InstrumentDetail.as_view(), name='instrument-detail'),
    path('categories/', InstrumentCategoryList.as_view(),
         name='instrument-category-list'),
    path('categories/<int:pk>/', InstrumentCategoryDetail.as_view(),
         name='instrument-category-detail')
]
