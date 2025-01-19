import logging
import requests
from celery import shared_task
from .models import Site, SiteStatusHistory, Webhook

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@shared_task
def check_site_status():
    logger.info("Starting task: check_site_status")
    sites = Site.objects.all()
    for site in sites:
        try:
            response = requests.get(site.url, timeout=10)
            current_status = 'up' if response.status_code == site.expected_status_code else 'down'
            response_time = response.elapsed.microseconds // 1000

            last_history = SiteStatusHistory.objects.filter(site=site).order_by('-checked_at').first()
            status_change = not last_history or last_history.status != current_status

            # Create history entry
            SiteStatusHistory.objects.create(
                site=site,
                status=current_status,
                response_time_ms=response_time,
                status_change=status_change
            )

            logger.info(f"Checked {site.name}: status={current_status}, response_time={response_time} ms, status_change={status_change}")

            # Notify if status changed (either up or down)
            if status_change:
                message = " 🟢 Site is back online." if current_status == 'up' else "Site is unreachable."
                notify_discord.delay(site.name, current_status, message)

        except requests.RequestException as e:
            current_status = 'down'
            response_time = 0
            
            # Check if this is a status change
            last_history = SiteStatusHistory.objects.filter(site=site).order_by('-checked_at').first()
            status_change = not last_history or last_history.status != current_status

            # Create history entry for error
            SiteStatusHistory.objects.create(
                site=site,
                status=current_status,
                response_time_ms=response_time,
                status_change=status_change
            )

            error_message = f"Error checking {site.name}: {str(e)}"
            logger.error(error_message)
            
            if status_change:
                notify_discord.delay(site.name, current_status, f" 🔴 Site is unreachable \nlog:{str(e)}")
    logger.info("Finished task: check_site_status")
    
@shared_task
def notify_discord(site_name, status, message):
    logger.info(f"Starting task: notify_discord for {site_name}")
    webhooks = Webhook.objects.all()
    data = {
        "content": f"Site {site_name} is {status}. {message}"
    }
    for webhook in webhooks:
        try:
            response = requests.post(webhook.url, json=data)
            response.raise_for_status()
            logger.info(f"Notification sent to Discord for {site_name}: {status}.")
        except requests.RequestException as e:
            logger.error(f"Failed to send notification to Discord for {site_name}: {e}")
    logger.info(f"Finished task: notify_discord for {site_name}")

@shared_task
def print_hello():
    print("Hello, world!")
    logger.info("Hello, world!")