from django.test import TestCase
from unittest.mock import patch, MagicMock
from .models import Site, Webhook, SiteStatusHistory
from .tasks import check_site_status, notify_discord

class DiscordNotificationTest(TestCase):
    def setUp(self):
        self.site = Site.objects.create(url="https://example.com", name="Test Site")
        self.webhook = Webhook.objects.create(url="https://discord.com/api/webhooks/test")

    @patch('monitor.tasks.requests.post')
    def test_notify_discord(self, mock_post):
        # Simulate a successful Discord notification
        mock_post.return_value.status_code = 204
        notify_discord(self.site.name, 'down', 'Test message')
        mock_post.assert_called_once_with(
            self.webhook.url,
            json={'content': f'**{self.site.name}** is now **down**.\nTest message'}
        )

    @patch('monitor.tasks.requests.get')
    def test_check_site_status(self, mock_get):
        # Simulate a successful response from the monitored site
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.microseconds = 123456  # Real response time in microseconds
        mock_get.return_value = mock_response
        
        # Call the check_site_status function to see if it handles the response correctly
        check_site_status()

        # Check if the status history was updated correctly
        site_history = SiteStatusHistory.objects.filter(site=self.site).first()
        self.assertIsNotNone(site_history)
        self.assertEqual(site_history.status, 'up')
        self.assertEqual(site_history.response_time_ms, 123)  # Microseconds converted to milliseconds
