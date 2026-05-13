from django.shortcuts import render
from .models import FAQItem


def faq_index(request):
    return render(request, 'faq/index.html', {
        'faq_items': FAQItem.objects.filter(is_active=True),
    })
