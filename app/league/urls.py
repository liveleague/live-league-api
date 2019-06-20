
# -------------------- Old API -------------------- #
'''
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('venues', views.VenueViewSet)
router.register('events', views.EventViewSet)
app_name = 'table'

urlpatterns = [
    path('', include(router.urls))
]
'''
