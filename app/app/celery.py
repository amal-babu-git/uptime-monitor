from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls check_site_status() every 10 minutes
    sender.add_periodic_task(600.0, sender.signature('monitor.tasks.check_site_status'), name='check site status every 10 minutes')
    # Calls print_hello() every minute
    sender.add_periodic_task(60.0, sender.signature('monitor.tasks.print_hello'), name='print hello every minute')

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')