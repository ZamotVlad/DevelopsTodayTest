from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TravelViewSet, PlaceViewSet

router = DefaultRouter()
router.register(r"travels", TravelViewSet, basename="travel")
router.register(r"places", PlaceViewSet, basename="place")

urlpatterns = [
    path("", include(router.urls)),
]
