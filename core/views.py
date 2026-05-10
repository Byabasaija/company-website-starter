from django.shortcuts import render, redirect
from django.utils import timezone
from .models import (HomepageSection, HeroSection, HeroSlide, HeroImage, AboutSection,
                     TeamMember, Service, Testimonial, Partner)
from blog.models import Blog
from events.models import Event
from gallery.models import GalleryImage
from faq.models import FAQItem


def home_view(request):
    now = timezone.now()
    context = {
        'homepage_sections': HomepageSection.objects.filter(is_active=True),
        'hero':         HeroSlide.objects.filter(is_active=True).first(),
        'hero_images':  HeroImage.objects.filter(is_active=True),
        'about':        AboutSection.objects.first(),
        'team_members': TeamMember.objects.filter(is_active=True),
        'services':     Service.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True),
        'partners':     Partner.objects.filter(is_active=True),
        'latest_blogs': Blog.objects.filter(draft=False).order_by('-datetime')[:3],
        'upcoming_events': Event.objects.filter(
            is_published=True, start_date__gte=now
        ).order_by('start_date')[:3],
        'gallery_images': GalleryImage.objects.filter(is_active=True)[:6],
        'faq_items':      FAQItem.objects.filter(is_active=True)[:5],
    }
    return render(request, 'home.html', context)


def about_view(request):
    return render(request, 'about.html', {
        'about':        AboutSection.objects.first(),
        'team_members': TeamMember.objects.filter(is_active=True),
    })


def services_view(request):
    return render(request, 'services.html', {
        'services': Service.objects.filter(is_active=True),
    })


def team_redirect(request):
    return redirect('about')
