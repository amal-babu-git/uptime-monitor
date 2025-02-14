from rest_framework import viewsets
from .models import Site, SiteStatusHistory, Webhook
from .serializers import SiteSerializer, SiteStatusHistorySerializer, WebhookSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS

# FIXME - Add permissions to the viewsets
class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminUser()]

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        site = self.get_object()
        history = SiteStatusHistory.objects.filter(site=site).order_by('-checked_at')
        serializer = SiteStatusHistorySerializer(history, many=True)
        return Response(serializer.data)

class WebhookViewSet(viewsets.ModelViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    permission_classes = [IsAuthenticated]