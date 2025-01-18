from django.contrib import admin
from .models import Site, SiteStatusHistory, Webhook
# Register your models here.
@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['url', 'name', 'check_interval_seconds', 'expected_status_code', 'created_at']

@admin.register(SiteStatusHistory)
class SiteStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['site', 'status', 'response_time_ms', 'checked_at', 'status_change']

@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ['url', 'description']