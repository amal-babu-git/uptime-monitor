from django.db import models

# FIXME: check interval feature not implemented
class Site(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    # check_interval_seconds = models.IntegerField(default=300)
    expected_status_code = models.IntegerField(default=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.url

class SiteStatusHistory(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=10, choices=[('up', 'Up'), ('down', 'Down')])
    response_time_ms = models.IntegerField()
    checked_at = models.DateTimeField(auto_now_add=True)
    status_change = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.site} - {self.status} - {self.checked_at}"

class Webhook(models.Model):
    url = models.URLField(unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.url