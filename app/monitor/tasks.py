import logging
import requests
from celery import shared_task
from .models import Site, SiteStatusHistory, Webhook

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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

            # Print statements for debugging
            print(f"Checked {site.name}: status={current_status}, response_time={response_time} ms, status_change={status_change}")
            logger.info(f"Checked {site.name}: status={current_status}, response_time={response_time} ms, status_change={status_change}")

            if current_status == 'down':
                notify_discord.delay(site.name, current_status, "Site is unreachable.")
        except Exception as e:
            print(f"Error checking {site.name}: {e}")
            logger.error(f"Error checking {site.name}: {e}. Site marked as down and notification sent.")

@shared_task
def notify_discord(site_name, status, message):
    print(f"Starting task: notify_discord for {site_name}")
    logger.info(f"Starting task: notify_discord for {site_name}")
    webhooks = Webhook.objects.all()
    data = {
        "content": f"Site {site_name} is {status}. {message}"
    }
    for webhook in webhooks:
        try:
            response = requests.post(webhook.url, json=data)
            response.raise_for_status()
            print(f"Notification sent to Discord for {site_name}: {status}")
            logger.info(f"Notification sent to Discord for {site_name}: {status}.")
        except requests.RequestException as e:
            print(f"Failed to send notification to Discord for {site_name}: {e}")
            logger.error(f"Failed to send notification to Discord for {site_name}: {e}")
    print(f"Finished task: notify_discord for {site_name}")
    logger.info(f"Finished task: notify_discord for {site_name}")

@shared_task
def print_hello():
    print("Hello, world!")
    logger.info("Hello, world!")