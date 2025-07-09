from django.urls import path
from .views import benchmark_api, metrics_api

urlpatterns = [
    path('benchmark/', benchmark_api, name='benchmark-api'),
    path('metrics/<int:result_id>/', metrics_api, name='metrics-api'),
]
