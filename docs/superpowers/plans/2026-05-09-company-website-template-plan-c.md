# Plan C — Company Website Template: Enhancements

**Status:** In progress  
**Created:** 2026-05-09  
**Depends on:** Plan A ✓, Plan B ✓

---

## Scope

Items 1–5 are general-purpose template enhancements. Item 6 (UCF customisation) is deferred to a separate plan once the generic template is complete.

---

## File Map

### Created
- `newsletter/` — full app (models, views, urls, admin, templates, tests)
- `templates/html/newsletter/subscribe_confirm.html`
- `templates/html/components/sections/newsletter.html`

### Modified
- `events/models.py` — description → HTMLField (Trix)
- `core/models.py` — AboutSection.body, Service.description → HTMLField (Trix)
- `templates/html/base.html` — Trix CDN, OG/canonical meta tags
- `templates/html/events/detail.html` — JSON-LD Event schema, OG image
- `templates/html/blog/blog-view.html` — JSON-LD Article schema, OG image
- `templates/html/home.html` — JSON-LD Organization schema
- `templates/html/gallery/index.html` — Alpine.js lightbox
- `templates/html/inquiry/inquiry-create.html` — reCAPTCHA v3
- `inquiry/views.py` — reCAPTCHA server-side verification
- `project/settings/base.py` — RECAPTCHA keys, NEWSLETTER settings
- `project/settings/development.py` — RECAPTCHA_SKIP_CHECK = True
- `project/urls.py` — newsletter routes
- `templates/css/output.css` — recompiled
- `project/settings/base.py` — `'newsletter'` in INSTALLED_APPS

---

## Task 1: Trix Rich-Text Editor

Trix is a standalone web component (no build step). Include via CDN, store HTML in TextField, render with `|safe`.

### Step 1 — Add Trix CDN to base.html
- Add in `{% block head_extra %}` (or directly in `<head>`):
  ```html
  <link rel="stylesheet" href="https://unpkg.com/trix@2/dist/trix.css">
  <script type="text/javascript" src="https://unpkg.com/trix@2/dist/trix.umd.min.js"></script>
  ```

### Step 2 — Create a custom TrixWidget for Django admin
Create `core/widgets.py`:
```python
from django import forms

class TrixWidget(forms.Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs['hidden'] = True
        textarea = super().render(name, value, attrs, renderer)
        editor_id = attrs.get('id', f'id_{name}')
        return (
            f'{textarea}'
            f'<trix-editor input="{editor_id}" class="trix-content border border-gray-300 rounded-lg min-h-[200px] p-2"></trix-editor>'
        )
    class Media:
        css = {'all': ['https://unpkg.com/trix@2/dist/trix.css']}
        js = ['https://unpkg.com/trix@2/dist/trix.umd.min.js']
```

### Step 3 — Apply widget in admin classes
- `events/admin.py` → `EventAdmin(forms.ModelForm)` with `widgets = {'description': TrixWidget()}`
- `core/admin.py` → `AboutSectionAdmin` with `widgets = {'body': TrixWidget()}`, `ServiceAdmin` with `widgets = {'description': TrixWidget()}`

### Step 4 — Render safely in templates
- `templates/html/events/detail.html` → `{{ event.description|safe }}` (already likely plain text — verify and update)
- `templates/html/about.html` → `{{ about.body|safe }}`
- `templates/html/services.html` → `{{ service.description|safe }}`

### Step 5 — Write tests
In `tests/test_trix.py`:
- `TrixWidgetTest` — widget renders `<trix-editor>` with correct `input` attribute
- `EventAdminTest` — EventAdmin uses TrixWidget for description field

### Step 6 — Commit
```
feat: add Trix rich-text editor widget for admin description fields
```

---

## Task 2: Newsletter Subscribe Form

### Step 1 — Write failing tests
Create `tests/test_newsletter.py` with:
- `SubscriberModelTest`: email unique, created_at auto, confirmed default False
- `SubscribeViewTest`: POST valid email → 200 + subscriber created; POST duplicate → error; GET → 200
- `UnsubscribeViewTest`: valid token → subscriber deleted; bad token → 404

### Step 2 — Create app
```
python manage.py startapp newsletter
```
Add `'newsletter'` to `INSTALLED_APPS` in `project/settings/base.py`.

### Step 3 — Write `newsletter/models.py`
```python
import uuid
from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
```

### Step 4 — Migration
```
python manage.py makemigrations newsletter
python manage.py migrate
```

### Step 5 — Write `newsletter/views.py`
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
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
```

### Step 6 — Write `newsletter/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.subscribe, name='newsletter-subscribe'),
    path('unsubscribe/<uuid:token>/', views.unsubscribe, name='newsletter-unsubscribe'),
]
```
Add to `project/urls.py`: `path('newsletter/', include('newsletter.urls'))`

### Step 7 — Write `newsletter/admin.py`
```python
from django.contrib import admin
from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'confirmed', 'created_at']
    list_filter = ['confirmed']
    readonly_fields = ['token', 'created_at']
```

### Step 8 — Templates
- `templates/html/newsletter/subscribed.html` — success message
- `templates/html/newsletter/unsubscribed.html` — unsubscribed message
- `templates/html/components/sections/newsletter.html` — inline subscribe form partial (for homepage/footer)

### Step 9 — Run tests, commit
```
feat: add newsletter subscribe/unsubscribe with Subscriber model and admin
```

---

## Task 3: SEO Enhancements

No new app — template and context changes only.

### Step 1 — Canonical URL tag in base.html
Add inside `<head>`:
```html
<link rel="canonical" href="{{ request.build_absolute_uri }}">
```
Ensure `django.template.context_processors.request` is in `TEMPLATES[0]['OPTIONS']['context_processors']`.

### Step 2 — OG image meta tags
In `base.html` add a `{% block og_image %}` with a default fallback:
```html
<meta property="og:image" content="{% block og_image %}{{ request.scheme }}://{{ request.get_host }}{% static 'img/og-default.png' %}{% endblock %}">
```
Override in:
- `events/detail.html` → `{% block og_image %}{{ request.scheme }}://{{ request.get_host }}{{ event.thumbnail.url }}{% endblock %}` (guarded by `{% if event.thumbnail %}`)
- `blog/blog-view.html` → same pattern with `blog.thumbnail`

### Step 3 — JSON-LD: Organization (homepage)
In `home.html` add `{% block structured_data %}`:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{{ site.site_name }}",
  "url": "{{ request.scheme }}://{{ request.get_host }}",
  "email": "{{ site.email }}"
}
</script>
```

### Step 4 — JSON-LD: Event (event detail)
In `events/detail.html`:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "{{ event.title }}",
  "startDate": "{{ event.start_date|date:'c' }}",
  {% if event.end_date %}"endDate": "{{ event.end_date|date:'c' }}",{% endif %}
  "location": { "@type": "Place", "name": "{{ event.location }}" },
  "url": "{{ request.build_absolute_uri }}"
}
</script>
```

### Step 5 — JSON-LD: Article (blog post)
In `blog/blog-view.html`:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{ blog.title }}",
  "datePublished": "{{ blog.datetime|date:'c' }}",
  "url": "{{ request.build_absolute_uri }}"
}
</script>
```

### Step 6 — Write tests
In `tests/test_seo.py`:
- Canonical tag present on homepage
- OG image tag present on event detail
- JSON-LD script tag present on homepage, event detail, blog post

### Step 7 — Commit
```
feat: add canonical URL, OG image tags, and JSON-LD structured data
```

---

## Task 4: Gallery Lightbox

Pure Alpine.js — no new library. Extend the existing gallery template.

### Step 1 — Wrap gallery page in Alpine store
In `templates/html/gallery/index.html`, add `x-data="galleryLightbox()"` on the outer div and define:
```html
<script>
function galleryLightbox() {
    return {
        open: false,
        src: '',
        caption: '',
        show(src, caption) { this.src = src; this.caption = caption; this.open = true; },
        close() { this.open = false; }
    }
}
</script>
```

### Step 2 — Make each image clickable
On each `<img>`, add: `@click="show('{{ image.image.url }}', '{{ image.caption }}')" class="cursor-pointer"`

### Step 3 — Add lightbox overlay
```html
<div x-show="open" x-cloak
     @keydown.escape.window="close()"
     @click.self="close()"
     class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4">
    <button @click="close()" class="absolute top-4 right-4 text-white text-3xl">&times;</button>
    <figure class="max-w-4xl w-full text-center">
        <img :src="src" class="max-h-[80vh] mx-auto rounded-lg object-contain">
        <figcaption x-text="caption" class="text-white mt-3 text-sm"></figcaption>
    </figure>
</div>
```

### Step 4 — Write tests
In `tests/test_gallery.py` (extend existing):
- `GalleryLightboxTest`: gallery page contains `@click="show(` and lightbox overlay markup

### Step 5 — Commit
```
feat: add Alpine.js lightbox to gallery page
```

---

## Task 5: Contact Form reCAPTCHA v3

### Step 1 — Add settings
In `project/settings/base.py`:
```python
RECAPTCHA_SITE_KEY = os.environ.get('RECAPTCHA_SITE_KEY', '')
RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY', '')
```
In `project/settings/development.py`:
```python
RECAPTCHA_SKIP_CHECK = True
```

### Step 2 — Add site key to context processor or template tag
Expose `RECAPTCHA_SITE_KEY` via the existing `site_config` context processor or a new template context var.

Add to `core/context_processors.py`:
```python
from django.conf import settings

def recaptcha(request):
    return {'RECAPTCHA_SITE_KEY': getattr(settings, 'RECAPTCHA_SITE_KEY', '')}
```
Register in `TEMPLATES[0]['OPTIONS']['context_processors']`.

### Step 3 — Update inquiry template
In `templates/html/inquiry/inquiry-create.html`:
- Add reCAPTCHA v3 script in `{% block scripts %}`:
  ```html
  {% if RECAPTCHA_SITE_KEY %}
  <script src="https://www.google.com/recaptcha/api.js?render={{ RECAPTCHA_SITE_KEY }}"></script>
  <script>
  document.querySelector('form').addEventListener('submit', function(e) {
      e.preventDefault();
      const form = this;
      grecaptcha.ready(() => {
          grecaptcha.execute('{{ RECAPTCHA_SITE_KEY }}', {action: 'inquiry'}).then(token => {
              let input = document.createElement('input');
              input.type = 'hidden'; input.name = 'g-recaptcha-response'; input.value = token;
              form.appendChild(input);
              form.submit();
          });
      });
  });
  </script>
  {% endif %}
  ```

### Step 4 — Server-side verification in inquiry view
In `inquiry/views.py`, in the POST handler:
```python
import requests as http_requests
from django.conf import settings

def _verify_recaptcha(token):
    if getattr(settings, 'RECAPTCHA_SKIP_CHECK', False):
        return True
    resp = http_requests.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': token,
    }).json()
    return resp.get('success') and resp.get('score', 0) >= 0.5
```
Call `_verify_recaptcha` before processing the form; return 400 if it fails.

### Step 5 — Write tests
In `tests/test_recaptcha.py`:
- `RecaptchaSkipTest`: with `RECAPTCHA_SKIP_CHECK=True`, inquiry form POST succeeds without token
- `RecaptchaBlockTest`: with `RECAPTCHA_SKIP_CHECK=False` and mock returning score 0.1, POST returns 400

### Step 6 — Commit
```
feat: add reCAPTCHA v3 to inquiry/contact form with dev skip flag
```

---

## Final Task: Recompile & Final Commit

```
./bin/tailwindcss -i styling/static_src/input.css -o templates/css/output.css --minify
python manage.py collectstatic --noinput
python manage.py test tests/ --verbosity=1
git add templates/css/output.css
git commit -m "chore: Plan C complete — Trix editor, newsletter, SEO, lightbox, reCAPTCHA; Tailwind recompiled"
```

---

## Self-Review Checklist

- [ ] Failing tests written before each implementation
- [ ] All existing 31 tests still pass after each task
- [ ] No placeholder code in templates
- [ ] Trix CDN only loads in admin (not public pages)
- [ ] reCAPTCHA skipped in development (no key required)
- [ ] JSON-LD renders valid schema.org markup
- [ ] Gallery lightbox closes on Escape and backdrop click
- [ ] Tailwind recompiled after all template changes
- [ ] One commit per task

---

## Deferred

**Item 6: Uganda Chess Federation features** (player profiles, tournament brackets, ratings table) — moved to a custom Plan D once the generic template is complete.
