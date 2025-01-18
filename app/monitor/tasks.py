import requests
from celery import shared_task
from .models import Site, SiteStatusHistory, Webhook

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


@shared_task
def notify_discord(site_name="monitor.amalbabu.live", status=200, message="test message"):
    webhooks = Webhook.objects.all()
    for webhook in webhooks:
        data = {
            "content": f"**{site_name}** is now **{status}**.\n{message}"
        }
        try:
            response = requests.post(webhook.url, json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            # Log or handle the error as needed
            print(f"Failed to send notification to Discord: {e}")

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

            if status_change:
                message = f"Response time: {response_time} ms" if current_status == 'up' else "No response."
                notify_discord.delay(site.name, current_status, message)

        except requests.RequestException:
            current_status = 'down'
            SiteStatusHistory.objects.create(
                site=site,
                status=current_status,
                response_time_ms=-1,
                status_change=True
            )
            notify_discord.delay(site.name, current_status, "Site is unreachable.")


#  to test -> python manage.py test