from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Page
from core.models import AboutSection, TeamMember, Service, Testimonial, Partner
from blog.models import Blog
from events.models import Event
from gallery.models import GalleryImage
from faq.models import FAQItem


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    now  = timezone.now()
    context = {
        'page':            page,
        'page_sections':   page.sections.filter(is_active=True),
        'about':           AboutSection.objects.first(),
        'team_members':    TeamMember.objects.filter(is_active=True),
        'services':        Service.objects.filter(is_active=True),
        'testimonials':    Testimonial.objects.filter(is_active=True),
        'partners':        Partner.objects.filter(is_active=True),
        'latest_blogs':    Blog.objects.filter(draft=False).order_by('-datetime')[:3],
        'upcoming_events': Event.objects.filter(
            is_published=True, start_date__gte=now
        ).order_by('start_date')[:3],
        'gallery_images':  GalleryImage.objects.filter(is_active=True)[:6],
        'faq_items':       FAQItem.objects.filter(is_active=True)[:5],
    }
    return render(request, 'pages/page.html', context)
