from django.urls import reverse
from django.contrib.sitemaps import Sitemap


class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    priority   = 0.9
    protocol   = 'https'

    def items(self):
        return ['home', 'about', 'services', 'event-list', 'gallery', 'faq', 'list-blogs']

    def location(self, item):
        return reverse(item)
