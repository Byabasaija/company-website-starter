from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from events.models import Event


def make_event(title, days_from_now, published=True, **kwargs):
    start = timezone.now() + timedelta(days=days_from_now)
    return Event.objects.create(
        title=title, start_date=start, is_published=published, **kwargs
    )


class EventModelTest(TestCase):

    def test_slug_auto_generated(self):
        e = make_event('Annual Chess Tournament', 5)
        self.assertEqual(e.slug, 'annual-chess-tournament')

    def test_slug_unique_on_duplicate_title(self):
        make_event('Open Championship', 1)
        e2 = Event.objects.create(
            title='Open Championship',
            start_date=timezone.now() + timedelta(days=2),
            is_published=True,
        )
        self.assertNotEqual(e2.slug, 'open-championship')

    def test_ordering_by_start_date(self):
        make_event('Later', 10)
        make_event('Sooner', 2)
        titles = list(Event.objects.values_list('title', flat=True))
        self.assertEqual(titles[0], 'Sooner')

    def test_unpublished_excluded_by_filter(self):
        make_event('Public', 1, published=True)
        make_event('Draft', 2, published=False)
        self.assertEqual(Event.objects.filter(is_published=True).count(), 1)


class EventViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_event_list_returns_200(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

    def test_event_detail_returns_200(self):
        e = make_event('Test Event', 3)
        response = self.client.get(f'/events/{e.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_event_detail_404_for_unpublished(self):
        e = make_event('Hidden', 3, published=False)
        response = self.client.get(f'/events/{e.slug}/')
        self.assertEqual(response.status_code, 404)

    def test_event_list_context_has_upcoming(self):
        make_event('Upcoming', 5)
        make_event('Past', -10)
        response = self.client.get('/events/')
        self.assertIn('upcoming_events', response.context)
        self.assertEqual(len(response.context['upcoming_events']), 1)
