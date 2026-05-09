from django.test import TestCase, Client
from django.utils import timezone
from core.models import SiteConfig
from events.models import Event
from blog.models import Blog


class CanonicalTagTest(TestCase):
    def setUp(self):
        self.client = Client()
        SiteConfig(site_name='Test Site').save()

    def test_homepage_has_canonical_tag(self):
        response = self.client.get('/')
        self.assertContains(response, '<link rel="canonical"')


class OGImageTagTest(TestCase):
    def setUp(self):
        self.client = Client()
        SiteConfig(site_name='Test Site').save()

    def test_base_has_og_image_meta(self):
        response = self.client.get('/')
        self.assertContains(response, 'property="og:image"')

    def test_event_detail_has_og_image_meta(self):
        event = Event.objects.create(
            title='Test Event',
            start_date=timezone.now(),
            is_published=True,
        )
        response = self.client.get(f'/events/{event.slug}/')
        self.assertContains(response, 'property="og:image"')


class JSONLDTest(TestCase):
    def setUp(self):
        self.client = Client()
        SiteConfig(site_name='Test Site').save()

    def test_homepage_has_organization_json_ld(self):
        response = self.client.get('/')
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, '"@type": "Organization"')

    def test_event_detail_has_event_json_ld(self):
        event = Event.objects.create(
            title='SEO Event',
            start_date=timezone.now(),
            is_published=True,
        )
        response = self.client.get(f'/events/{event.slug}/')
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, '"@type": "Event"')

    def test_blog_detail_has_article_json_ld(self):
        post = Blog.objects.create(
            title='SEO Post',
            body='Hello world',
            draft=False,
        )
        response = self.client.get(f'/blog/{post.slug}/')
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, '"@type": "Article"')
