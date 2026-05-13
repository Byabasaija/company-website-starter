from unittest.mock import patch
from django.test import TestCase, Client, override_settings
from django.urls import reverse


@override_settings(RECAPTCHA_SKIP_CHECK=True)
class RecaptchaSkipTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_inquiry_post_succeeds_without_token_when_skip_enabled(self):
        response = self.client.post(reverse('contact-us'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Hello there',
            'inquiry_type': 'general',
        })
        self.assertIn(response.status_code, [200, 302])

    def test_inquiry_page_loads(self):
        response = self.client.get(reverse('contact-us'))
        self.assertEqual(response.status_code, 200)


class RecaptchaSiteKeyContextTest(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(RECAPTCHA_SITE_KEY='test-key-abc')
    def test_recaptcha_site_key_in_context(self):
        response = self.client.get(reverse('contact-us'))
        self.assertEqual(response.context.get('RECAPTCHA_SITE_KEY'), 'test-key-abc')

    @override_settings(RECAPTCHA_SITE_KEY='')
    def test_recaptcha_site_key_empty_when_not_set(self):
        response = self.client.get(reverse('contact-us'))
        self.assertEqual(response.context.get('RECAPTCHA_SITE_KEY', ''), '')
