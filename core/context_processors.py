from django.conf import settings
from .models import SiteConfig


def site_config(request):
    try:
        site = SiteConfig.objects.get(pk=1)
    except SiteConfig.DoesNotExist:
        site = SiteConfig(site_name='My Company')

    # NavLink and FooterLink are added in a later migration;
    # import them lazily to avoid errors before migrations run.
    try:
        from .models import NavLink, FooterLink
        nav_links = NavLink.objects.filter(is_active=True)
        footer_links = FooterLink.objects.filter(is_active=True)
    except Exception:
        nav_links = []
        footer_links = []

    return {
        'site': site,
        'nav_links': nav_links,
        'footer_links': footer_links,
        'GOOGLE_ANALYTICS': getattr(settings, 'GOOGLE_ANALYTICS', ''),
    }
