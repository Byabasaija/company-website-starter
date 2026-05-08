from django.conf import settings
from .models import SiteConfig, NavLink, FooterLink


def site_config(request):
    try:
        site = SiteConfig.objects.get(pk=1)
    except SiteConfig.DoesNotExist:
        site = SiteConfig(site_name='My Company')

    return {
        'site': site,
        'nav_links': NavLink.objects.filter(is_active=True),
        'footer_links': FooterLink.objects.filter(is_active=True),
        'GOOGLE_ANALYTICS': getattr(settings, 'GOOGLE_ANALYTICS', ''),
    }
