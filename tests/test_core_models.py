from django.test import TestCase
from core.models import SiteConfig, HomepageSection


class SiteConfigSingletonTest(TestCase):

    def test_save_always_uses_pk_1(self):
        config = SiteConfig(site_name='Test Site')
        config.save()
        self.assertEqual(config.pk, 1)

    def test_second_save_overwrites_not_creates(self):
        SiteConfig(site_name='First').save()
        SiteConfig(site_name='Second').save()
        self.assertEqual(SiteConfig.objects.count(), 1)
        self.assertEqual(SiteConfig.objects.get(pk=1).site_name, 'Second')


class HomepageSectionOrderingTest(TestCase):

    def test_sections_ordered_by_order_field(self):
        HomepageSection.objects.create(section_type='about', order=2, is_active=True)
        HomepageSection.objects.create(section_type='hero', order=1, is_active=True)
        sections = list(HomepageSection.objects.all())
        self.assertEqual(sections[0].section_type, 'hero')
        self.assertEqual(sections[1].section_type, 'about')

    def test_inactive_sections_excluded_when_filtered(self):
        HomepageSection.objects.create(section_type='hero', order=1, is_active=True)
        HomepageSection.objects.create(section_type='about', order=2, is_active=False)
        active = HomepageSection.objects.filter(is_active=True)
        self.assertEqual(active.count(), 1)
        self.assertEqual(active.first().section_type, 'hero')
