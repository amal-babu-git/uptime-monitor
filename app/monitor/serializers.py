from rest_framework import serializers
from .models import Site, SiteStatusHistory, Webhook

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'url', 'name', 'expected_status_code', ]

class SiteStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteStatusHistory
        fields = ['status', 'response_time_ms', 'status_change']


class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = ['id', 'url', 'description', 'created_at']