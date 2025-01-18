# monitoring/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SiteViewSet, WebhookViewSet

router = DefaultRouter()
router.register('sites', SiteViewSet)
router.register('webhooks', WebhookViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
