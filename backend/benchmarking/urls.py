from django.urls import path
from .views import TraductionList, TraductionDetail

urlpatterns = [
    path('traductions/', TraductionList.as_view(), name='traduction-list'),
    path('traductions/<int:pk>', TraductionDetail.as_view(), name='traduction-detail'),
]