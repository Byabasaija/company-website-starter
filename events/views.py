from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Event


def event_list(request):
    now = timezone.now()
    upcoming = Event.objects.filter(is_published=True, start_date__gte=now).order_by('start_date')
    past     = Event.objects.filter(is_published=True, start_date__lt=now).order_by('-start_date')
    return render(request, 'events/list.html', {
        'upcoming_events': upcoming,
        'past_events':     past,
    })


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    return render(request, 'events/detail.html', {'event': event})
