from django.urls import path
from .views import InstrumentList, InstrumentDetail

urlpatterns = [
    path('', InstrumentList.as_view(), name='instrument-list'),
    path('<int:pk>/', InstrumentDetail.as_view(), name='instrument-detail')
]
