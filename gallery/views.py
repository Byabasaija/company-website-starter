from django.shortcuts import render
from .models import GalleryCategory, GalleryImage


def gallery_index(request):
    categories = GalleryCategory.objects.all()
    images     = GalleryImage.objects.filter(is_active=True).select_related('category')
    return render(request, 'gallery/index.html', {
        'categories': categories,
        'images':     images,
    })
