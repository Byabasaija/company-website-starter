from django.conf import settings
from .models import SiteConfig, NavLink


def site_config(request):
    try:
        site = SiteConfig.objects.get(pk=1)
    except SiteConfig.DoesNotExist:
        site = SiteConfig(site_name='My Company')

    return {
        'site': site,
        'nav_links': NavLink.objects.filter(
            is_active=True, parent=None, placement__in=['primary', 'both']
        ).prefetch_related('children'),
        'footer_links': NavLink.objects.filter(
            is_active=True, placement__in=['footer', 'both']
        ),
        'GOOGLE_ANALYTICS': getattr(settings, 'GOOGLE_ANALYTICS', ''),
        'RECAPTCHA_SITE_KEY': getattr(settings, 'RECAPTCHA_SITE_KEY', ''),
    }
