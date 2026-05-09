# Company Website Template — Plan B: Events, Gallery, FAQ

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the three content apps that complete the homepage section stubs left by Plan A — `events`, `gallery`, and `faq`. Wire each into the home view context, fill in the stub partials, add `/events/`, `/gallery/`, and `/faq/` pages, update sitemaps and nav defaults.

**Prerequisite:** Plan A complete (all 13 tasks merged on `main`).

**Spec:** `docs/superpowers/specs/2026-05-08-company-website-template-design.md`

**Plan A:** `docs/superpowers/plans/2026-05-08-company-website-template-plan-a.md`

---

## File Map

### Created
```
events/__init__.py
events/apps.py
events/models.py
events/admin.py
events/views.py
events/urls.py
events/sitemaps.py
events/migrations/0001_initial.py        (auto-generated)
gallery/__init__.py
gallery/apps.py
gallery/models.py
gallery/admin.py
gallery/views.py
gallery/urls.py
gallery/migrations/0001_initial.py       (auto-generated)
faq/__init__.py
faq/apps.py
faq/models.py
faq/admin.py
faq/views.py
faq/urls.py
faq/migrations/0001_initial.py           (auto-generated)
templates/html/events/list.html
templates/html/events/detail.html
templates/html/gallery/index.html
templates/html/faq/index.html
tests/test_events.py
tests/test_gallery.py
tests/test_faq.py
```

### Modified
```
project/settings/base.py                 (add events, gallery, faq to INSTALLED_APPS)
project/urls.py                          (add events/, gallery/, faq/ routes; EventSitemap)
project/sitemaps.py                      (add about, services, events-list, gallery, faq to StaticSitemap)
core/views.py                            (replace stub [] with real querysets)
core/migrations/0005_nav_events_link.py  (hand-written — adds Events nav link)
templates/html/components/sections/upcoming-events.html   (fill stub)
templates/html/components/sections/gallery-preview.html   (fill stub)
templates/html/components/sections/faq-preview.html       (fill stub)
```

---

## Task 1: `events` app

**Models:** `Event` — title, slug, description, start_date, end_date (blank), location (blank), thumbnail (blank), is_published (default False), created_at (auto).

### Step 1 — Write failing tests

Create `tests/test_events.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from events.models import Event


def make_event(title, days_from_now, published=True, **kwargs):
    start = timezone.now() + timedelta(days=days_from_now)
    return Event.objects.create(
        title=title, start_date=start, is_published=published, **kwargs
    )


class EventModelTest(TestCase):

    def test_slug_auto_generated(self):
        e = make_event('Annual Chess Tournament', 5)
        self.assertEqual(e.slug, 'annual-chess-tournament')

    def test_slug_unique_on_duplicate_title(self):
        make_event('Open Championship', 1)
        e2 = Event.objects.create(
            title='Open Championship',
            start_date=timezone.now() + timedelta(days=2),
            is_published=True,
        )
        self.assertNotEqual(e2.slug, 'open-championship')

    def test_ordering_by_start_date(self):
        make_event('Later', 10)
        make_event('Sooner', 2)
        titles = list(Event.objects.values_list('title', flat=True))
        self.assertEqual(titles[0], 'Sooner')

    def test_unpublished_excluded_by_filter(self):
        make_event('Public', 1, published=True)
        make_event('Draft', 2, published=False)
        self.assertEqual(Event.objects.filter(is_published=True).count(), 1)


class EventViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_event_list_returns_200(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

    def test_event_detail_returns_200(self):
        e = make_event('Test Event', 3)
        response = self.client.get(f'/events/{e.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_event_detail_404_for_unpublished(self):
        e = make_event('Hidden', 3, published=False)
        response = self.client.get(f'/events/{e.slug}/')
        self.assertEqual(response.status_code, 404)

    def test_event_list_context_has_upcoming(self):
        make_event('Upcoming', 5)
        make_event('Past', -10)
        response = self.client.get('/events/')
        self.assertIn('upcoming_events', response.context)
        self.assertEqual(len(response.context['upcoming_events']), 1)
```

- [ ] **Step 1: Run tests — expect ImportError**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_events -v 2
```
Expected: `ModuleNotFoundError: No module named 'events'`

---

### Step 2 — Create the app

```bash
python manage.py startapp events
```

- [ ] **Step 2a: Write `events/apps.py`**

```python
from django.apps import AppConfig

class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'
```

- [ ] **Step 2b: Write `events/models.py`**

```python
from django.db import models
from django.utils.text import slugify


class Event(models.Model):
    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True, blank=True)
    description  = models.TextField(blank=True)
    start_date   = models.DateTimeField()
    end_date     = models.DateTimeField(blank=True, null=True)
    location     = models.CharField(max_length=200, blank=True)
    thumbnail    = models.ImageField(upload_to='events/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Event.objects.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)
```

- [ ] **Step 2c: Add to `INSTALLED_APPS` in `project/settings/base.py`**

```python
    # first party
    'core',
    'user',
    'blog',
    'inquiry',
    'events',
    'gallery',
    'faq',
```

(Add all three now — gallery and faq come in later tasks but adding them here avoids a second settings edit.)

- [ ] **Step 2d: Create and run migration**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py makemigrations events
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py migrate
```

- [ ] **Step 2e: Run model tests — expect pass**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_events.EventModelTest -v 2
```
Expected: `Ran 4 tests ... OK`

---

### Step 3 — Admin

- [ ] **Step 3: Write `events/admin.py`**

```python
from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ('title', 'start_date', 'location', 'is_published')
    list_editable = ('is_published',)
    list_filter   = ('is_published',)
    ordering      = ('start_date',)
    prepopulated_fields = {'slug': ('title',)}
```

---

### Step 4 — Views and URLs

- [ ] **Step 4a: Write `events/views.py`**

```python
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
```

- [ ] **Step 4b: Write `events/urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('',        views.event_list,   name='event-list'),
    path('<slug:slug>/', views.event_detail, name='event-detail'),
]
```

- [ ] **Step 4c: Add to `project/urls.py`**

Add below the existing app includes:

```python
    path('events/',  include('events.urls')),
    path('gallery/', include('gallery.urls')),
    path('faq/',     include('faq.urls')),
```

Also update `StaticSitemap.items()` later in Task 4.

- [ ] **Step 4d: Run view tests**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_events.EventViewTest -v 2
```
Expected: `Ran 4 tests ... OK`

---

### Step 5 — Templates

- [ ] **Step 5a: Create `templates/html/events/list.html`**

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Events{% endblock %}
{% block description %}Upcoming and past events from {{ site.site_name }}{% endblock %}

{% block content %}
<section class="section-padding">
    <div class="max-w-7xl mx-auto">
        <h1 class="section-title">Events</h1>

        {% if upcoming_events %}
        <h2 class="text-xl font-semibold text-gray-700 mb-6">Upcoming</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
            {% for event in upcoming_events %}
            <a href="{% url 'event-detail' slug=event.slug %}" class="card hover:shadow-md transition-shadow group">
                {% if event.thumbnail %}
                <div class="aspect-video overflow-hidden">
                    <img src="{{ event.thumbnail.url }}" alt="{{ event.title }}"
                         class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                </div>
                {% endif %}
                <div class="p-6">
                    <p class="text-primary text-sm font-medium mb-1">
                        {{ event.start_date|date:"N j, Y" }}
                        {% if event.end_date %} – {{ event.end_date|date:"N j, Y" }}{% endif %}
                    </p>
                    <h3 class="font-semibold text-gray-900 text-lg mb-2 group-hover:text-primary transition-colors leading-snug">
                        {{ event.title }}
                    </h3>
                    {% if event.location %}
                    <p class="text-gray-500 text-sm flex items-center gap-1">
                        <i class="bi bi-geo-alt"></i> {{ event.location }}
                    </p>
                    {% endif %}
                </div>
            </a>
            {% endfor %}
        </div>
        {% else %}
        <p class="text-gray-500 text-center py-10">No upcoming events at this time.</p>
        {% endif %}

        {% if past_events %}
        <h2 class="text-xl font-semibold text-gray-700 mb-6 border-t border-gray-100 pt-10">Past Events</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {% for event in past_events %}
            <a href="{% url 'event-detail' slug=event.slug %}"
               class="card hover:shadow-md transition-shadow group opacity-75 hover:opacity-100">
                {% if event.thumbnail %}
                <div class="aspect-video overflow-hidden">
                    <img src="{{ event.thumbnail.url }}" alt="{{ event.title }}"
                         class="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-300">
                </div>
                {% endif %}
                <div class="p-6">
                    <p class="text-gray-400 text-sm font-medium mb-1">
                        {{ event.start_date|date:"N j, Y" }}
                    </p>
                    <h3 class="font-semibold text-gray-700 text-lg mb-2 leading-snug">{{ event.title }}</h3>
                    {% if event.location %}
                    <p class="text-gray-400 text-sm flex items-center gap-1">
                        <i class="bi bi-geo-alt"></i> {{ event.location }}
                    </p>
                    {% endif %}
                </div>
            </a>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</section>
{% endblock %}
```

- [ ] **Step 5b: Create `templates/html/events/detail.html`**

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ event.title }}{% endblock %}
{% block description %}{{ event.description|truncatewords:30 }}{% endblock %}

{% block content %}
<article class="section-padding">
    <div class="max-w-3xl mx-auto">

        <header class="mb-10">
            <div class="flex flex-wrap items-center gap-3 text-sm text-primary font-medium mb-4">
                <span class="flex items-center gap-1">
                    <i class="bi bi-calendar3"></i>
                    {{ event.start_date|date:"N j, Y, g:i A" }}
                    {% if event.end_date %} – {{ event.end_date|date:"N j, Y, g:i A" }}{% endif %}
                </span>
                {% if event.location %}
                <span class="flex items-center gap-1 text-gray-500">
                    <i class="bi bi-geo-alt"></i> {{ event.location }}
                </span>
                {% endif %}
            </div>
            <h1 class="text-4xl lg:text-5xl font-bold text-gray-900 leading-tight">{{ event.title }}</h1>
        </header>

        {% if event.thumbnail %}
        <div class="rounded-2xl overflow-hidden shadow-md mb-10 aspect-video">
            <img src="{{ event.thumbnail.url }}" alt="{{ event.title }}"
                 class="w-full h-full object-cover">
        </div>
        {% endif %}

        {% if event.description %}
        <div class="text-gray-700 leading-relaxed prose max-w-none">
            {{ event.description|linebreaks }}
        </div>
        {% endif %}

        <div class="mt-12 pt-8 border-t border-gray-100">
            <a href="{% url 'event-list' %}" class="text-primary font-medium hover:underline flex items-center gap-1">
                <i class="bi bi-arrow-left"></i> All events
            </a>
        </div>
    </div>
</article>
{% endblock %}
```

- [ ] **Step 5c: Fill in `templates/html/components/sections/upcoming-events.html`**

```html
{% load static %}
{% if upcoming_events %}
<section class="section-padding bg-white">
    <div class="max-w-7xl mx-auto">
        <div class="flex items-center justify-between mb-10">
            <h2 class="section-title mb-0">Upcoming Events</h2>
            <a href="/events/" class="text-primary font-semibold hover:underline text-sm flex items-center gap-1">
                All events <i class="bi bi-arrow-right"></i>
            </a>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {% for event in upcoming_events %}
            <a href="{% url 'event-detail' slug=event.slug %}" class="card hover:shadow-md transition-shadow group">
                {% if event.thumbnail %}
                <div class="aspect-video overflow-hidden">
                    <img src="{{ event.thumbnail.url }}" alt="{{ event.title }}"
                         class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                </div>
                {% endif %}
                <div class="p-6">
                    <p class="text-primary text-sm font-medium mb-1">{{ event.start_date|date:"N j, Y" }}</p>
                    <h3 class="font-semibold text-gray-900 text-lg group-hover:text-primary transition-colors leading-snug mb-1">
                        {{ event.title }}
                    </h3>
                    {% if event.location %}
                    <p class="text-gray-500 text-sm flex items-center gap-1">
                        <i class="bi bi-geo-alt"></i> {{ event.location }}
                    </p>
                    {% endif %}
                </div>
            </a>
            {% endfor %}
        </div>
    </div>
</section>
{% endif %}
```

- [ ] **Step 5d: Commit events app**

```bash
git add events/ templates/html/events/ templates/html/components/sections/upcoming-events.html tests/test_events.py project/settings/base.py project/urls.py
git commit -m "feat: add events app — model, admin, views, templates, homepage partial"
```

---

## Task 2: `gallery` app

**Models:** `GalleryCategory` (name, slug, order), `GalleryImage` (category FK, image, caption, order, is_active).

### Step 1 — Write failing tests

Create `tests/test_gallery.py`:

```python
from django.test import TestCase, Client
from gallery.models import GalleryCategory, GalleryImage


def make_category(name, order=0):
    from django.utils.text import slugify
    return GalleryCategory.objects.create(name=name, slug=slugify(name), order=order)


class GalleryCategoryTest(TestCase):

    def test_categories_ordered_by_order(self):
        make_category('Chess Boards', order=2)
        make_category('Tournaments', order=1)
        cats = list(GalleryCategory.objects.values_list('name', flat=True))
        self.assertEqual(cats[0], 'Tournaments')

    def test_slug_stored(self):
        cat = make_category('Annual Cup')
        self.assertEqual(cat.slug, 'annual-cup')


class GalleryImageTest(TestCase):

    def setUp(self):
        self.cat = make_category('General')

    def test_active_images_filtered(self):
        GalleryImage.objects.create(category=self.cat, image='gallery/a.jpg', order=1, is_active=True)
        GalleryImage.objects.create(category=self.cat, image='gallery/b.jpg', order=2, is_active=False)
        self.assertEqual(GalleryImage.objects.filter(is_active=True).count(), 1)

    def test_images_ordered_by_order(self):
        GalleryImage.objects.create(category=self.cat, image='gallery/b.jpg', order=2, is_active=True)
        GalleryImage.objects.create(category=self.cat, image='gallery/a.jpg', order=1, is_active=True)
        imgs = list(GalleryImage.objects.all())
        self.assertEqual(imgs[0].order, 1)


class GalleryViewTest(TestCase):

    def test_gallery_returns_200(self):
        response = self.client.get('/gallery/')
        self.assertEqual(response.status_code, 200)

    def test_gallery_context_has_images_and_categories(self):
        response = self.client.get('/gallery/')
        self.assertIn('images', response.context)
        self.assertIn('categories', response.context)
```

- [ ] **Step 1: Run tests — expect ImportError**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_gallery -v 2
```
Expected: `ModuleNotFoundError: No module named 'gallery'`

---

### Step 2 — Create the app

```bash
python manage.py startapp gallery
```

- [ ] **Step 2a: Write `gallery/apps.py`**

```python
from django.apps import AppConfig

class GalleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gallery'
```

- [ ] **Step 2b: Write `gallery/models.py`**

```python
from django.db import models


class GalleryCategory(models.Model):
    name  = models.CharField(max_length=100)
    slug  = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Gallery categories'

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE,
                                  related_name='images')
    image    = models.ImageField(upload_to='gallery/')
    caption  = models.CharField(max_length=200, blank=True)
    order    = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.caption or str(self.image)
```

- [ ] **Step 2c: Migrations** (`gallery` was already added to INSTALLED_APPS in Task 1 Step 2c)

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py makemigrations gallery
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py migrate
```

- [ ] **Step 2d: Run model tests**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_gallery.GalleryCategoryTest tests.test_gallery.GalleryImageTest -v 2
```
Expected: `Ran 4 tests ... OK`

---

### Step 3 — Admin

- [ ] **Step 3: Write `gallery/admin.py`**

```python
from django.contrib import admin
from .models import GalleryCategory, GalleryImage


class GalleryImageInline(admin.TabularInline):
    model  = GalleryImage
    extra  = 3
    fields = ('image', 'caption', 'order', 'is_active')


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GalleryImageInline]


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display  = ('__str__', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('category', 'is_active')
```

---

### Step 4 — Views and URLs

- [ ] **Step 4a: Write `gallery/views.py`**

```python
from django.shortcuts import render
from .models import GalleryCategory, GalleryImage


def gallery_index(request):
    categories = GalleryCategory.objects.all()
    images     = GalleryImage.objects.filter(is_active=True).select_related('category')
    return render(request, 'gallery/index.html', {
        'categories': categories,
        'images':     images,
    })
```

- [ ] **Step 4b: Write `gallery/urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_index, name='gallery'),
]
```

- [ ] **Step 4c: Run view tests**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_gallery.GalleryViewTest -v 2
```
Expected: `Ran 2 tests ... OK`

---

### Step 5 — Templates

- [ ] **Step 5a: Create `templates/html/gallery/index.html`**

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Gallery{% endblock %}
{% block description %}Photo gallery from {{ site.site_name }}{% endblock %}

{% block content %}
<section class="section-padding"
         x-data="{ filter: 'all' }">
    <div class="max-w-7xl mx-auto">
        <h1 class="section-title text-center">Gallery</h1>

        {% if categories %}
        <div class="flex flex-wrap justify-center gap-2 mb-10">
            <button @click="filter = 'all'"
                    :class="filter === 'all' ? 'bg-primary text-white' : 'bg-white text-gray-600 border border-gray-300 hover:border-primary hover:text-primary'"
                    class="px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                All
            </button>
            {% for category in categories %}
            <button @click="filter = '{{ category.slug }}'"
                    :class="filter === '{{ category.slug }}' ? 'bg-primary text-white' : 'bg-white text-gray-600 border border-gray-300 hover:border-primary hover:text-primary'"
                    class="px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                {{ category.name }}
            </button>
            {% endfor %}
        </div>
        {% endif %}

        {% if images %}
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {% for image in images %}
            <div x-show="filter === 'all' || filter === '{{ image.category.slug }}'"
                 x-transition:enter="transition ease-out duration-200"
                 x-transition:enter-start="opacity-0 scale-95"
                 x-transition:enter-end="opacity-100 scale-100"
                 class="aspect-square overflow-hidden rounded-xl shadow-sm group">
                <img src="{{ image.image.url }}"
                     alt="{{ image.caption|default:image.category.name }}"
                     class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                     loading="lazy">
            </div>
            {% endfor %}
        </div>
        {% else %}
        <p class="text-center text-gray-500 py-16">No images yet.</p>
        {% endif %}
    </div>
</section>
{% endblock %}
```

- [ ] **Step 5b: Fill in `templates/html/components/sections/gallery-preview.html`**

```html
{% load static %}
{% if gallery_images %}
<section class="section-padding bg-surface">
    <div class="max-w-7xl mx-auto">
        <div class="flex items-center justify-between mb-10">
            <h2 class="section-title mb-0">Gallery</h2>
            <a href="/gallery/" class="text-primary font-semibold hover:underline text-sm flex items-center gap-1">
                View all <i class="bi bi-arrow-right"></i>
            </a>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            {% for image in gallery_images %}
            <a href="/gallery/" class="aspect-square overflow-hidden rounded-xl shadow-sm group">
                <img src="{{ image.image.url }}"
                     alt="{{ image.caption|default:'' }}"
                     class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                     loading="lazy">
            </a>
            {% endfor %}
        </div>
    </div>
</section>
{% endif %}
```

- [ ] **Step 5c: Commit gallery app**

```bash
git add gallery/ templates/html/gallery/ templates/html/components/sections/gallery-preview.html tests/test_gallery.py
git commit -m "feat: add gallery app — models, admin, Alpine.js filter grid, homepage partial"
```

---

## Task 3: `faq` app

**Model:** `FAQItem` — question, answer, order, is_active.

### Step 1 — Write failing tests

Create `tests/test_faq.py`:

```python
from django.test import TestCase, Client
from faq.models import FAQItem


class FAQItemTest(TestCase):

    def test_active_items_ordered(self):
        FAQItem.objects.create(question='Q2', answer='A2', order=2, is_active=True)
        FAQItem.objects.create(question='Q1', answer='A1', order=1, is_active=True)
        items = list(FAQItem.objects.filter(is_active=True))
        self.assertEqual(items[0].question, 'Q1')

    def test_inactive_excluded(self):
        FAQItem.objects.create(question='Q-active', answer='A', order=1, is_active=True)
        FAQItem.objects.create(question='Q-hidden', answer='A', order=2, is_active=False)
        self.assertEqual(FAQItem.objects.filter(is_active=True).count(), 1)


class FAQViewTest(TestCase):

    def test_faq_returns_200(self):
        response = self.client.get('/faq/')
        self.assertEqual(response.status_code, 200)

    def test_faq_context_has_items(self):
        FAQItem.objects.create(question='Q', answer='A', order=1, is_active=True)
        response = self.client.get('/faq/')
        self.assertIn('faq_items', response.context)
        self.assertEqual(len(response.context['faq_items']), 1)
```

- [ ] **Step 1: Run tests — expect ImportError**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_faq -v 2
```
Expected: `ModuleNotFoundError: No module named 'faq'`

---

### Step 2 — Create the app

```bash
python manage.py startapp faq
```

- [ ] **Step 2a: Write `faq/apps.py`**

```python
from django.apps import AppConfig

class FaqConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faq'
```

- [ ] **Step 2b: Write `faq/models.py`**

```python
from django.db import models


class FAQItem(models.Model):
    question  = models.CharField(max_length=300)
    answer    = models.TextField()
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering  = ['order']
        verbose_name      = 'FAQ Item'
        verbose_name_plural = 'FAQ Items'

    def __str__(self):
        return self.question
```

- [ ] **Step 2c: Migrations** (`faq` was already added to INSTALLED_APPS in Task 1 Step 2c)

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py makemigrations faq
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py migrate
```

- [ ] **Step 2d: Run model tests**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_faq.FAQItemTest -v 2
```
Expected: `Ran 2 tests ... OK`

---

### Step 3 — Admin

- [ ] **Step 3: Write `faq/admin.py`**

```python
from django.contrib import admin
from .models import FAQItem


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display  = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
```

---

### Step 4 — Views and URLs

- [ ] **Step 4a: Write `faq/views.py`**

```python
from django.shortcuts import render
from .models import FAQItem


def faq_index(request):
    return render(request, 'faq/index.html', {
        'faq_items': FAQItem.objects.filter(is_active=True),
    })
```

- [ ] **Step 4b: Write `faq/urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.faq_index, name='faq'),
]
```

- [ ] **Step 4c: Run view tests**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_faq.FAQViewTest -v 2
```
Expected: `Ran 2 tests ... OK`

---

### Step 5 — Templates

- [ ] **Step 5a: Create `templates/html/faq/index.html`**

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}FAQ{% endblock %}
{% block description %}Frequently asked questions about {{ site.site_name }}{% endblock %}

{% block content %}
<section class="section-padding">
    <div class="max-w-3xl mx-auto">
        <h1 class="section-title text-center">Frequently Asked Questions</h1>
        <p class="section-subtitle text-center">Answers to common questions</p>

        {% if faq_items %}
        <div class="divide-y divide-gray-200 border border-gray-200 rounded-xl overflow-hidden mt-4">
            {% for item in faq_items %}
            <div x-data="{ open: false }">
                <button @click="open = !open"
                        class="w-full flex items-center justify-between px-6 py-5 text-left hover:bg-gray-50 transition-colors">
                    <span class="font-semibold text-gray-900 pr-4">{{ item.question }}</span>
                    <i class="bi text-primary shrink-0 transition-transform duration-200"
                       :class="open ? 'bi-dash-circle' : 'bi-plus-circle'"></i>
                </button>
                <div x-show="open"
                     x-transition:enter="transition ease-out duration-200"
                     x-transition:enter-start="opacity-0 -translate-y-1"
                     x-transition:enter-end="opacity-100 translate-y-0"
                     class="px-6 pb-5 text-gray-600 leading-relaxed">
                    {{ item.answer|linebreaks }}
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <p class="text-center text-gray-500 py-16">No FAQ items yet.</p>
        {% endif %}
    </div>
</section>
{% endblock %}
```

- [ ] **Step 5b: Fill in `templates/html/components/sections/faq-preview.html`**

```html
{% if faq_items %}
<section class="section-padding bg-white">
    <div class="max-w-3xl mx-auto">
        <div class="flex items-center justify-between mb-10">
            <h2 class="section-title mb-0">FAQ</h2>
            <a href="/faq/" class="text-primary font-semibold hover:underline text-sm flex items-center gap-1">
                All questions <i class="bi bi-arrow-right"></i>
            </a>
        </div>
        <div class="divide-y divide-gray-200 border border-gray-200 rounded-xl overflow-hidden">
            {% for item in faq_items %}
            <div x-data="{ open: false }">
                <button @click="open = !open"
                        class="w-full flex items-center justify-between px-6 py-4 text-left hover:bg-gray-50 transition-colors">
                    <span class="font-medium text-gray-900 pr-4">{{ item.question }}</span>
                    <i class="bi text-primary shrink-0 transition-transform duration-200"
                       :class="open ? 'bi-dash-circle' : 'bi-plus-circle'"></i>
                </button>
                <div x-show="open"
                     x-transition:enter="transition ease-out duration-200"
                     x-transition:enter-start="opacity-0 -translate-y-1"
                     x-transition:enter-end="opacity-100 translate-y-0"
                     class="px-6 pb-4 text-gray-600 text-sm leading-relaxed">
                    {{ item.answer|linebreaks }}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endif %}
```

- [ ] **Step 5c: Commit faq app**

```bash
git add faq/ templates/html/faq/ templates/html/components/sections/faq-preview.html tests/test_faq.py
git commit -m "feat: add faq app — model, admin, Alpine.js accordion, homepage partial"
```

---

## Task 4: Wire new apps into home view + sitemaps

### Step 1 — Update `core/views.py`

Replace the stub empty lists with real querysets. The events, gallery, and faq apps now exist.

- [ ] **Step 1: Rewrite `core/views.py` home_view context**

```python
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import (HomepageSection, HeroSection, AboutSection,
                     TeamMember, Service, Testimonial, Partner)
from blog.models import Blog
from events.models import Event
from gallery.models import GalleryImage
from faq.models import FAQItem


def home_view(request):
    now = timezone.now()
    context = {
        'homepage_sections': HomepageSection.objects.filter(is_active=True),
        'hero':         HeroSection.objects.first(),
        'about':        AboutSection.objects.first(),
        'team_members': TeamMember.objects.filter(is_active=True),
        'services':     Service.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True),
        'partners':     Partner.objects.filter(is_active=True),
        'latest_blogs': Blog.objects.filter(draft=False).order_by('-datetime')[:3],
        'upcoming_events': Event.objects.filter(
            is_published=True, start_date__gte=now
        ).order_by('start_date')[:3],
        'gallery_images': GalleryImage.objects.filter(is_active=True)[:6],
        'faq_items':    FAQItem.objects.filter(is_active=True)[:5],
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
```

---

### Step 2 — Update sitemaps

- [ ] **Step 2a: Create `events/sitemaps.py`**

```python
from django.contrib.sitemaps import Sitemap
from .models import Event


class EventSitemap(Sitemap):
    changefreq = 'weekly'
    priority   = 0.7
    protocol   = 'https'

    def items(self):
        return Event.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return f'/events/{obj.slug}/'
```

- [ ] **Step 2b: Update `project/sitemaps.py`**

```python
from datetime import datetime
from django.urls import reverse
from django.contrib.sitemaps import Sitemap


class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    priority   = 0.9
    protocol   = 'https'

    def items(self):
        return ['home', 'about', 'services', 'event-list', 'gallery', 'faq', 'list-blogs']

    def location(self, item):
        return reverse(item)
```

- [ ] **Step 2c: Add `EventSitemap` to `project/urls.py`**

```python
from events.sitemaps import EventSitemap

sitemap_dict = {
    'sitemaps': {
        'static': StaticSitemap,
        'blog':   BlogSitemap,
        'events': EventSitemap,
    }
}
```

---

### Step 3 — Add Events nav link via data migration

The spec calls for Events as a default nav link. Add it without disturbing existing nav data.

- [ ] **Step 3: Create `core/migrations/0005_nav_events_link.py`**

```python
from django.db import migrations


def add_events_nav(apps, schema_editor):
    NavLink = apps.get_model('core', 'NavLink')
    if not NavLink.objects.filter(url='/events/').exists():
        # Shift Blog (3→4) and Contact (4→5) to make room
        NavLink.objects.filter(label='Blog').update(order=4)
        NavLink.objects.filter(label='Contact').update(order=5)
        NavLink.objects.create(label='Events', url='/events/', order=3, is_active=True)


def remove_events_nav(apps, schema_editor):
    NavLink = apps.get_model('core', 'NavLink')
    NavLink.objects.filter(url='/events/').delete()
    NavLink.objects.filter(label='Blog').update(order=3)
    NavLink.objects.filter(label='Contact').update(order=4)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_default_data'),
    ]
    operations = [
        migrations.RunPython(add_events_nav, remove_events_nav),
    ]
```

- [ ] **Step 3: Run migration**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py migrate
```

---

### Step 4 — Run full test suite

- [ ] **Step 4: Verify all tests pass**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests -v 2
```
Expected: all tests pass (13 from Plan A + 8 from events + 6 from gallery + 4 from faq = 31 tests).

- [ ] **Step 4: Commit wiring**

```bash
git add core/views.py core/migrations/0005_nav_events_link.py events/sitemaps.py project/sitemaps.py project/urls.py
git commit -m "feat: wire events/gallery/faq into home view, sitemaps, and nav migration"
```

---

## Task 5: Final compilation and smoke test

- [ ] **Step 1: Recompile Tailwind**

```bash
./bin/tailwindcss -i styling/static_src/input.css -o templates/css/output.css --minify
```

New classes used in Plan B templates: `divide-y`, `divide-gray-200`, `grayscale`, `grayscale-0`, `aspect-square`, `bi-plus-circle`, `bi-dash-circle`, `bi-geo-alt`, `bi-calendar3`. Verify output is updated.

- [ ] **Step 2: Run collectstatic**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py collectstatic --noinput 2>&1 | tail -5
```
Expected: no errors.

- [ ] **Step 3: Smoke test all pages**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py runserver
```

Visit each URL and verify 200, correct layout, no broken CSS or JS:

| URL | Expected |
|---|---|
| `http://127.0.0.1:8000/` | Homepage; events/gallery/faq sections visible if HomepageSection rows are active |
| `http://127.0.0.1:8000/events/` | Events list; "No upcoming events" if empty |
| `http://127.0.0.1:8000/gallery/` | Gallery grid; category filter buttons (Alpine.js) |
| `http://127.0.0.1:8000/faq/` | FAQ accordion (Alpine.js open/close) |
| `http://127.0.0.1:8000/admin/` | All new apps appear: Events, Gallery Categories, Gallery Images, FAQ Items |
| `http://127.0.0.1:8000/sitemap.xml` | Contains events and static URLs |

- [ ] **Step 4: Run full test suite one last time**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests -v 2
```
Expected: all tests pass.

- [ ] **Step 5: Final commit**

```bash
git add templates/css/output.css
git commit -m "chore: Plan B complete — events, gallery, faq apps; Tailwind recompiled"
```

---

## Self-Review Checklist

- [ ] **Spec coverage:** `events` app ✓, `gallery` app ✓, `faq` app ✓, homepage partials filled ✓, `/events/`, `/gallery/`, `/faq/` routes ✓, Events nav link migration ✓, EventSitemap ✓, StaticSitemap updated ✓, Alpine.js gallery filter ✓, Alpine.js FAQ accordion ✓, TDD throughout ✓
- [ ] **No placeholders:** All steps have complete code
- [ ] **Stub partials replaced:** `upcoming-events.html`, `gallery-preview.html`, `faq-preview.html` all filled in
- [ ] **home_view context updated:** `upcoming_events`, `gallery_images`, `faq_items` use real queries

---

## What Plan C Could Cover

- Trix rich-text editor integration in admin (events description, about body)
- Newsletter subscribe form with backend (Mailchimp / local model)
- SEO enhancements: per-page OG images, canonical URLs, structured data (JSON-LD for events)
- Multi-image lightbox on gallery page
- Contact form reCAPTCHA
- Chess-specific features for Uganda Chess Federation (player profiles, tournament brackets, ratings)
