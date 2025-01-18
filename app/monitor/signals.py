from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Webhook
from .tasks import notify_discord

# Signal handler to send welcome message after a new Webhook is added
@receiver(post_save, sender=Webhook)
def send_welcome_message_on_webhook_addition(sender, instance, created, **kwargs):
    if created:
        notify_discord(site_name="monitor.amalbabu.live", status=200, message="Welcome to the monitoring service!")
