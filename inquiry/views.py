import json
import urllib.parse
import urllib.request
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from django_ratelimit.decorators import ratelimit

from .models import Inquiry
from .forms import InquiryForm


def _verify_recaptcha(token):
    if getattr(settings, 'RECAPTCHA_SKIP_CHECK', False):
        return True
    if not token:
        return False
    try:
        data = urllib.parse.urlencode({
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': token,
        }).encode()
        with urllib.request.urlopen(
            'https://www.google.com/recaptcha/api/siteverify', data, timeout=5
        ) as r:
            resp = json.loads(r.read().decode())
        return resp.get('success') and resp.get('score', 0) >= 0.5
    except Exception:
        return False


@require_http_methods(['GET', 'POST'])
def inquiry_view(request):  

    if request.method == 'GET':

        return render(request, 'inquiry/inquiry-create.html')
    
    elif request.method == 'POST':

        token = request.POST.get('g-recaptcha-response', '')
        if not _verify_recaptcha(token):
            return render(request, 'inquiry/inquiry-create.html', {
                'errors': {'recaptcha': ['Please complete the reCAPTCHA verification.']},
                'data': request.POST,
            })

        form = InquiryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("contact-success")

        return render(request, 'inquiry/inquiry-create.html', {
                'errors': form.errors,
                'data': request.POST,
        })
    

@require_http_methods(['POST'])
@ratelimit(key='ip', rate='10/min', method=ratelimit.ALL, block=True)
def inquiry_api_view(request):
    

    form = InquiryForm(request.POST)

    if form.is_valid():
        form.save(commit=False)
        
        return JsonResponse({'success': 'inquiry submitted'}, status=200)

    else:
        # print("errors: ", form.errors, form.non_field_errors)
        return JsonResponse({'error': 'invalid data error'}, status=400)


@require_http_methods(['GET'])
def inquiry_success(request):

    return render(request, "components/pages/success.html", {
        'title': 'Inquiry Submitted', 
        'description': 'Thank you for taking time to submit an inquiry, our team will be in touch shortly.'
    })