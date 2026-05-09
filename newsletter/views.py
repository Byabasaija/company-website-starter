from django.shortcuts import render, get_object_or_404
from .models import Subscriber


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            Subscriber.objects.get_or_create(email=email)
        return render(request, 'newsletter/subscribed.html')
    return render(request, 'newsletter/subscribe.html')


def unsubscribe(request, token):
    sub = get_object_or_404(Subscriber, token=token)
    sub.delete()
    return render(request, 'newsletter/unsubscribed.html')
