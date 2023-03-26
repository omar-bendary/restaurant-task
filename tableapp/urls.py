from django.urls import path, include
from rest_framework import routers
from .views import TableViewSet, ReservationViewSet


router = routers.DefaultRouter()
router.register('tables', TableViewSet)
router.register('reservations', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
