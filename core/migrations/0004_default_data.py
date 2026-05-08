from django.db import migrations


def create_defaults(apps, schema_editor):
    SiteConfig = apps.get_model('core', 'SiteConfig')
    HomepageSection = apps.get_model('core', 'HomepageSection')
    NavLink = apps.get_model('core', 'NavLink')
    FooterLink = apps.get_model('core', 'FooterLink')
    HeroSection = apps.get_model('core', 'HeroSection')
    AboutSection = apps.get_model('core', 'AboutSection')

    SiteConfig.objects.get_or_create(pk=1, defaults={
        'site_name': 'My Company',
        'tagline': 'Your tagline here',
        'primary_color': '#1a56a0',
        'secondary_color': '#f5a623',
        'footer_text': '© 2026 My Company. All rights reserved.',
    })

    sections = [
        ('hero',         1),
        ('about',        2),
        ('services',     3),
        ('team',         4),
        ('events',       5),
        ('gallery',      6),
        ('testimonials', 7),
        ('partners',     8),
        ('news',         9),
        ('faq',         10),
    ]
    for section_type, order in sections:
        HomepageSection.objects.get_or_create(
            section_type=section_type,
            defaults={'order': order, 'is_active': True},
        )

    nav_defaults = [
        ('Home',     '/',         1),
        ('About',    '/about/',   2),
        ('Blog',     '/blog/',    3),
        ('Contact',  '/contact/', 4),
    ]
    for label, url, order in nav_defaults:
        NavLink.objects.get_or_create(label=label, defaults={'url': url, 'order': order, 'is_active': True})

    footer_defaults = [
        ('Home',           '/',               1),
        ('About',          '/about/',         2),
        ('Contact',        '/contact/',       3),
        ('Privacy Policy', '/privacy/',       4),
    ]
    for label, url, order in footer_defaults:
        FooterLink.objects.get_or_create(label=label, defaults={'url': url, 'order': order, 'is_active': True})

    HeroSection.objects.get_or_create(pk=1, defaults={
        'headline': 'Welcome to Our Organisation',
        'subheadline': 'Empowering communities through excellence.',
        'cta_text': 'Learn More',
        'cta_url': '/about/',
    })

    AboutSection.objects.get_or_create(pk=1, defaults={
        'heading': 'About Us',
        'body': 'We are a dedicated organisation committed to our mission.',
    })


def reverse_defaults(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_footerlink_navlink'),
    ]
    operations = [
        migrations.RunPython(create_defaults, reverse_defaults),
    ]
