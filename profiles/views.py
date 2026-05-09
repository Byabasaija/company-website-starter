from django.shortcuts import render, get_object_or_404
from .models import Profile, ProfileCategory


def profile_list(request):
    return render(request, 'profiles/list.html', {
        'profiles':   Profile.objects.filter(is_active=True).select_related('category'),
        'categories': ProfileCategory.objects.all(),
    })


def profile_detail(request, slug):
    profile = get_object_or_404(Profile, slug=slug, is_active=True)
    return render(request, 'profiles/detail.html', {'profile': profile})
