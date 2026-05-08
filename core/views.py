from django.shortcuts import render, redirect
from .models import (HomepageSection, HeroSection, AboutSection,
                     TeamMember, Service, Testimonial, Partner)
from blog.models import Blog


def home_view(request):
    context = {
        'homepage_sections': HomepageSection.objects.filter(is_active=True),
        'hero':         HeroSection.objects.first(),
        'about':        AboutSection.objects.first(),
        'team_members': TeamMember.objects.filter(is_active=True),
        'services':     Service.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True),
        'partners':     Partner.objects.filter(is_active=True),
        'latest_blogs': Blog.objects.filter(draft=False).order_by('-datetime')[:3],
        'upcoming_events': [],
        'gallery_images':  [],
        'faq_items':       [],
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
