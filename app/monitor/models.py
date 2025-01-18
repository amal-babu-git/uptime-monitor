from django.db import models

class Site(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    check_interval_seconds = models.IntegerField(default=300)
    expected_status_code = models.IntegerField(default=200)
    created_at = models.DateTimeField(auto_now_add=True)

class SiteStatusHistory(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=10, choices=[('up', 'Up'), ('down', 'Down')])
    response_time_ms = models.IntegerField()
    checked_at = models.DateTimeField(auto_now_add=True)
    status_change = models.BooleanField(default=False)
