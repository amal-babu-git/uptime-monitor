import requests
from celery import shared_task
from .models import Site, SiteStatusHistory

@shared_task
def check_site_status():
    sites = Site.objects.all()
    for site in sites:
        try:
            response = requests.get(site.url, timeout=10)
            current_status = 'up' if response.status_code == site.expected_status_code else 'down'
            response_time = response.elapsed.microseconds // 1000

            last_history = SiteStatusHistory.objects.filter(site=site).order_by('-checked_at').first()
            status_change = not last_history or last_history.status != current_status

            SiteStatusHistory.objects.create(
                site=site,
                status=current_status,
                response_time_ms=response_time,
                status_change=status_change
            )
        except requests.RequestException:
            current_status = 'down'
            response_time = -1
            SiteStatusHistory.objects.create(
                site=site,
                status=current_status,
                response_time_ms=response_time,
                status_change=True
            )
