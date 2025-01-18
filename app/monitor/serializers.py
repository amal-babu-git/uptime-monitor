from rest_framework import serializers
from .models import Site, SiteStatusHistory

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'url', 'name', 'check_interval_seconds', 'expected_status_code', 'created_at']

class SiteStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteStatusHistory
        fields = ['status', 'response_time_ms', 'checked_at', 'status_change']
