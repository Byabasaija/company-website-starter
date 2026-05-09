from django.test import TestCase, Client
from django.urls import reverse


class SubscriberModelTest(TestCase):
    def test_email_is_unique(self):
        from newsletter.models import Subscriber
        from django.db import IntegrityError
        Subscriber.objects.create(email='a@example.com')
        with self.assertRaises(IntegrityError):
            Subscriber.objects.create(email='a@example.com')

    def test_confirmed_defaults_false(self):
        from newsletter.models import Subscriber
        sub = Subscriber.objects.create(email='b@example.com')
        self.assertFalse(sub.confirmed)

    def test_token_auto_generated(self):
        from newsletter.models import Subscriber
        sub = Subscriber.objects.create(email='c@example.com')
        self.assertIsNotNone(sub.token)

    def test_str_returns_email(self):
        from newsletter.models import Subscriber
        sub = Subscriber.objects.create(email='d@example.com')
        self.assertEqual(str(sub), 'd@example.com')


class SubscribeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_returns_200(self):
        response = self.client.get(reverse('newsletter-subscribe'))
        self.assertEqual(response.status_code, 200)

    def test_post_valid_email_creates_subscriber(self):
        from newsletter.models import Subscriber
        self.client.post(reverse('newsletter-subscribe'), {'email': 'new@example.com'})
        self.assertTrue(Subscriber.objects.filter(email='new@example.com').exists())

    def test_post_valid_email_returns_200(self):
        response = self.client.post(reverse('newsletter-subscribe'), {'email': 'x@example.com'})
        self.assertEqual(response.status_code, 200)

    def test_post_duplicate_email_does_not_error(self):
        from newsletter.models import Subscriber
        Subscriber.objects.create(email='dup@example.com')
        response = self.client.post(reverse('newsletter-subscribe'), {'email': 'dup@example.com'})
        self.assertEqual(response.status_code, 200)


class UnsubscribeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_token_deletes_subscriber(self):
        from newsletter.models import Subscriber
        sub = Subscriber.objects.create(email='unsub@example.com')
        self.client.get(reverse('newsletter-unsubscribe', args=[sub.token]))
        self.assertFalse(Subscriber.objects.filter(email='unsub@example.com').exists())

    def test_valid_token_returns_200(self):
        from newsletter.models import Subscriber
        sub = Subscriber.objects.create(email='unsub2@example.com')
        response = self.client.get(reverse('newsletter-unsubscribe', args=[sub.token]))
        self.assertEqual(response.status_code, 200)

    def test_invalid_token_returns_404(self):
        import uuid
        response = self.client.get(reverse('newsletter-unsubscribe', args=[uuid.uuid4()]))
        self.assertEqual(response.status_code, 404)
