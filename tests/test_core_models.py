from django.test import TestCase
from core.models import SiteConfig, HomepageSection, HeroSection, AboutSection, TeamMember, Service, Testimonial, Partner


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


class HeroSectionTest(TestCase):
    def test_create_hero(self):
        hero = HeroSection.objects.create(
            headline='Welcome',
            subheadline='We are here',
            cta_text='Learn more',
            cta_url='/about/',
        )
        self.assertEqual(HeroSection.objects.count(), 1)
        self.assertEqual(hero.headline, 'Welcome')


class TeamMemberTest(TestCase):
    def test_team_members_ordered_by_order_field(self):
        TeamMember.objects.create(name='Bob', role='CEO', order=2, is_active=True)
        TeamMember.objects.create(name='Alice', role='CTO', order=1, is_active=True)
        members = list(TeamMember.objects.filter(is_active=True))
        self.assertEqual(members[0].name, 'Alice')

    def test_inactive_members_excluded(self):
        TeamMember.objects.create(name='Active', role='CEO', order=1, is_active=True)
        TeamMember.objects.create(name='Inactive', role='CFO', order=2, is_active=False)
        self.assertEqual(TeamMember.objects.filter(is_active=True).count(), 1)
