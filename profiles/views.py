from django.shortcuts import render, get_object_or_404
from .models import Profile, ProfileCategory


def profile_list(request):
    categories = ProfileCategory.objects.all()
    return render(request, 'profiles/list.html', {'categories': categories})


def profile_category(request, category_slug):
    category = get_object_or_404(ProfileCategory, slug=category_slug)
    profiles  = Profile.objects.filter(category=category, is_active=True)
    return render(request, 'profiles/category.html', {
        'category': category,
        'profiles': profiles,
    })


def profile_detail(request, category_slug, profile_slug):
    category = get_object_or_404(ProfileCategory, slug=category_slug)
    profile  = get_object_or_404(Profile, slug=profile_slug, category=category, is_active=True)
    return render(request, 'profiles/detail.html', {
        'profile':  profile,
        'category': category,
    })
