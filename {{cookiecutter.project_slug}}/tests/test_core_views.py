from django.test import TestCase, Client
from core.models import SiteConfig, HomepageSection, AboutSection


class HomepageViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        SiteConfig(site_name='Test Site').save()
        HomepageSection.objects.all().delete()
        HomepageSection.objects.create(section_type='hero', order=1, is_active=True)
        HomepageSection.objects.create(section_type='about', order=2, is_active=False)
        AboutSection.objects.all().delete()
        AboutSection.objects.create(heading='About', body='We exist.')

    def test_homepage_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_context_has_site(self):
        response = self.client.get('/')
        self.assertIn('site', response.context)
        self.assertEqual(response.context['site'].site_name, 'Test Site')

    def test_homepage_context_has_active_sections(self):
        response = self.client.get('/')
        sections = list(response.context['homepage_sections'])
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].section_type, 'hero')

    def test_about_page_returns_200(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_services_page_returns_200(self):
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)
