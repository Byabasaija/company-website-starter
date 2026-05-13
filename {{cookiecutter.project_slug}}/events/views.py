from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Event


def event_list(request):
    now = timezone.now()
    # Upcoming: hasn't ended yet (use end_date if set, otherwise start_date)
    upcoming = Event.objects.filter(is_published=True).filter(
        Q(end_date__gte=now) | Q(end_date__isnull=True, start_date__gte=now)
    ).order_by('start_date')
    # Past: already ended
    past = Event.objects.filter(is_published=True).filter(
        Q(end_date__lt=now) | Q(end_date__isnull=True, start_date__lt=now)
    ).order_by('-start_date')
    return render(request, 'events/list.html', {
        'upcoming_events': upcoming,
        'past_events':     past,
    })


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    return render(request, 'events/detail.html', {'event': event})
