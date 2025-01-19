import logging
import requests
from celery import shared_task
from .models import Site, SiteStatusHistory, Webhook
from django.utils import timezone

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@shared_task
def check_site_status():
    logger.info("Starting task: check_site_status")
    sites = Site.objects.all()
    
    for site in sites:
        current_status = 'down'
        response_time = 0
        error_message = None
        current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        try:
            response = requests.get(site.url, timeout=10)
            current_status = 'up' if response.status_code == site.expected_status_code else 'down'
            response_time = response.elapsed.microseconds // 1000
        except requests.RequestException as e:
            error_message = str(e)
            logger.error(f"Error checking {site.name}: {error_message}")

        # Check status change and get last history
        last_history = SiteStatusHistory.objects.filter(site=site).order_by('-checked_at').first()
        status_change = not last_history or last_history.status != current_status

        # Create history entry
        SiteStatusHistory.objects.create(
            site=site,
            status=current_status,
            response_time_ms=response_time,
            status_change=status_change
        )

        if status_change:
            if current_status == 'up':
                # Calculate downtime duration
                downtime = ""
                if last_history and last_history.status == 'down':
                    delta = timezone.now() - last_history.checked_at
                    minutes = int(delta.total_seconds() // 60)
                    downtime = f"\nDowntime Duration: {minutes} minutes"
                
                message = (
                    f"🟢 Website Recovery Alert\n"
                    f"Site: {site.name} ({site.url})\n"
                    f"Status: UP\n"
                    f"Time: {current_time}"
                    f"{downtime}"
                )
            else:
                message = (
                    f"🔴 Website Down Alert\n"
                    f"Site: {site.name} ({site.url})\n"
                    f"Status: DOWN\n"
                    f"Time: {current_time}\n"
                    f"Error: {error_message if error_message else 'Unexpected status code'}"
                )
            
            notify_discord.delay(site.name, current_status, message)
            logger.info(f"Status change detected for {site.name}: {current_status}")

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