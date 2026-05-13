from django.contrib.sitemaps import Sitemap
from .models import Event


class EventSitemap(Sitemap):
    changefreq = 'weekly'
    priority   = 0.7
    protocol   = 'https'

    def items(self):
        return Event.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return f'/events/{obj.slug}/'
