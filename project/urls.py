from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.shortcuts import render

from project.sitemaps import StaticSitemap
from blog.sitemaps import BlogSitemap
from project.views import rate_limiter_view, view_404, handler_403

admin.site.site_header = 'Site Admin'
admin.site.index_title = 'Dashboard'
admin.site.site_title = 'Admin'
admin.site.site_url = '/'

handler404 = view_404
handler403 = handler_403

sitemap_dict = {'sitemaps': {'static': StaticSitemap, 'blog': BlogSitemap}}

urlpatterns = [
    path('admin/',   admin.site.urls),
    path('',         include('core.urls')),
    path('blog/',    include('blog.urls')),
    path('contact/', include('inquiry.urls')),
    path('user/',    include('user.urls')),

    path('sitemap.xml', sitemap, sitemap_dict, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('ratelimit-error/', rate_limiter_view, name='ratelimit-error'),
]

if settings.DEBUG:
    urlpatterns += [path('__reload__/', include('django_browser_reload.urls'))]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [re_path(r'^.*/$', view_404, name='page_not_found')]
