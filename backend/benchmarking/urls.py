from django.urls import path
from .views import TraductionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('traductions', TraductionViewSet, basename='traductions')

urlpatterns = router.urls
