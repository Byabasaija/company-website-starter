# Company Website Template — Design Spec

**Date:** 2026-05-08
**Project:** Django-website-template → resellable company website starter
**First use case:** Uganda Chess Federation

---

## Overview

Extend the existing Django starter into a fully admin-driven, resellable company website template. A buyer (e.g. a chess federation, NGO, local business) receives a working site where all content, branding, section order, and navigation are managed from Django admin — no code editing required post-deploy.

The template must deploy on cPanel's "Run Python Application" (Passenger WSGI) as the primary target, while remaining deployable on Railway/Render/DigitalOcean via the existing Procfile.

---

## Tech Stack Changes

| Layer | From | To |
|---|---|---|
| Django | 4.2.11 | 5.2 LTS |
| CSS framework | django-tailwind 3 + Bootstrap CSS + `tw-` prefix | Tailwind CSS v4 standalone CLI, no prefix |
| JS interactivity | Bootstrap JS (CDN) | Alpine.js (CDN) |
| Icons | Bootstrap Icons | Bootstrap Icons (keep, CDN only) |
| Media storage | Google Cloud Storage (hardwired) | Local disk default, S3/GCS opt-in via env var |
| Settings structure | Single `settings.py` with Firebase imports | Split: `base.py` / `development.py` / `production.py` |
| Deployment | Gunicorn only | `passenger_wsgi.py` (cPanel) + Procfile (PaaS) |

---

## App Structure

```
project/           Django project config
core/              NEW — SiteConfig, homepage sections, nav/footer links
events/            NEW — Event model
gallery/           NEW — GalleryCategory, GalleryImage
faq/               NEW — FAQItem
blog/              keep (minor cleanup)
inquiry/           keep (contact form)
user/              keep
```

---

## Data Models

### `core` app

#### `SiteConfig` (singleton)
| Field | Type | Notes |
|---|---|---|
| site_name | CharField(100) | |
| tagline | CharField(200) | |
| logo | ImageField | |
| favicon | ImageField | |
| primary_color | CharField(7) | hex, e.g. `#1a56a0` |
| secondary_color | CharField(7) | hex |
| email | EmailField | |
| phone | CharField(20) | |
| address | TextField | |
| footer_text | CharField(200) | copyright line |
| facebook | URLField blank | |
| twitter | URLField blank | |
| instagram | URLField blank | |
| linkedin | URLField blank | |
| youtube | URLField blank | |

Enforced as singleton: `save()` always uses `pk=1`; `has_delete_permission` returns `False` in the admin; `has_add_permission` returns `False` once a row exists. Admin shows it as a change form, not a list.

#### `HomepageSection`
Controls which sections appear on the homepage and in what order.

| Field | Type | Notes |
|---|---|---|
| section_type | CharField choices | hero, about, services, team, events, gallery, testimonials, partners, news, faq |
| order | PositiveIntegerField | sort key |
| is_active | BooleanField | show/hide on homepage |

`unique=True` on `section_type`. Pre-populated via data migration with all 10 sections in a sensible default order. `Meta.ordering = ['order']`.

#### `HeroSection`
| Field | Type |
|---|---|
| headline | CharField(200) |
| subheadline | CharField(300) |
| cta_text | CharField(50) |
| cta_url | CharField(200) |
| background_image | ImageField |

#### `AboutSection`
| Field | Type |
|---|---|
| heading | CharField(200) |
| body | TextField (Trix rich text in admin) |
| image | ImageField blank |

#### `TeamMember`
| Field | Type |
|---|---|
| name | CharField(100) |
| role | CharField(100) |
| photo | ImageField blank |
| bio | TextField blank |
| order | PositiveIntegerField |
| is_active | BooleanField |
| facebook / twitter / linkedin | URLField blank |

#### `Service`
| Field | Type |
|---|---|
| title | CharField(100) |
| description | TextField |
| icon | CharField(50) — Bootstrap icon name |
| order | PositiveIntegerField |
| is_active | BooleanField |

#### `Testimonial`
| Field | Type |
|---|---|
| name | CharField(100) |
| role | CharField(100) blank |
| organization | CharField(100) blank |
| quote | TextField |
| photo | ImageField blank |
| order | PositiveIntegerField |
| is_active | BooleanField |

#### `Partner`
| Field | Type |
|---|---|
| name | CharField(100) |
| logo | ImageField |
| website_url | URLField blank |
| order | PositiveIntegerField |
| is_active | BooleanField |

#### `NavLink`
| Field | Type |
|---|---|
| label | CharField(50) |
| url | CharField(200) |
| order | PositiveIntegerField |
| is_active | BooleanField |

Pre-populated: Home, About, Events, Blog, Contact. `Meta.ordering = ['order']`.

#### `FooterLink`
Same shape as `NavLink`. Pre-populated: Home, About, Contact, Privacy Policy.

---

### `events` app

#### `Event`
| Field | Type |
|---|---|
| title | CharField(200) |
| slug | SlugField unique |
| description | TextField (Trix rich text in admin) |
| start_date | DateTimeField |
| end_date | DateTimeField blank |
| location | CharField(200) blank |
| thumbnail | ImageField blank |
| is_published | BooleanField default False |
| created_at | DateTimeField auto |

---

### `gallery` app

#### `GalleryCategory`
| Field | Type |
|---|---|
| name | CharField(100) |
| slug | SlugField unique |
| order | PositiveIntegerField |

#### `GalleryImage`
| Field | Type |
|---|---|
| category | ForeignKey GalleryCategory |
| image | ImageField |
| caption | CharField(200) blank |
| order | PositiveIntegerField |
| is_active | BooleanField |

---

### `faq` app

#### `FAQItem`
| Field | Type |
|---|---|
| question | CharField(300) |
| answer | TextField |
| order | PositiveIntegerField |
| is_active | BooleanField |

---

### `blog` app (unchanged)
`Blog`: blog_id, user(FK), thumbnail, slug, title, body, draft, datetime
`BlogImage`: blog(FK), image

---

### `inquiry` app (unchanged)
`Inquiry`: name, email, phone, inquiry_type, description, datetime

---

## URL Structure

```
/                          homepage
/about/                    standalone About page (AboutSection content + active TeamMembers)
/team/                     alias for /about/ — redirects there
/services/                 standalone Services page (all active Service rows)
/events/                   event list
/events/<slug>/            event detail
/gallery/                  gallery grid (filterable by category)
/blog/                     blog list (paginated)
/blog/<slug>/              blog post detail
/faq/                      FAQ accordion page
/contact/                  contact form
/contact/success/          post-submit success page
/admin/                    Django admin
/sitemap.xml
/robots.txt
/ratelimit-error/
```

---

## Template Structure

```
templates/html/
├── base.html                        navbar (NavLinks), footer (FooterLinks + SiteConfig)
├── home.html                        loops HomepageSection, includes section partials
├── components/
│   └── sections/
│       ├── hero.html
│       ├── about.html
│       ├── services.html
│       ├── team.html
│       ├── upcoming-events.html     3 nearest future events
│       ├── gallery-preview.html     latest 6 images
│       ├── testimonials.html        Alpine.js carousel
│       ├── partners.html
│       ├── latest-news.html         3 latest published blogs
│       └── faq-preview.html         first 5 FAQ items
├── about.html                       full about + team page
├── team.html
├── services.html
├── events/
│   ├── list.html
│   └── detail.html
├── gallery/
│   └── index.html                   Alpine.js category filter
├── blog/
│   ├── blog-list.html
│   └── blog-view.html
├── faq/
│   └── index.html                   Alpine.js accordion
├── inquiry/
│   ├── contact.html
│   └── success.html
└── error/
    ├── 404.html
    └── ratelimit.html
```

### Context processor
`core.context_processors.site_config` runs on every request:
- Loads `SiteConfig` (cached after first query)
- Loads active `NavLink` list
- Loads active `FooterLink` list
- Injects as `{{ site }}`, `{{ nav_links }}`, `{{ footer_links }}`

### Homepage assembly
`home.html` iterates `HomepageSection.objects.filter(is_active=True)` (ordered by `order`) and uses `{% if section.section_type == 'hero' %}{% include ... %}{% endif %}` blocks to include the right partial. Each partial receives the relevant queryset/object via the view context.

---

## Frontend Details

### Tailwind v4 setup
- Standalone CLI binary at `bin/tailwindcss` (gitignored binary, documented in README)
- Source: `styling/static_src/input.css`
- Output: `styling/static_src/output.css` (committed to repo)
- Dev command: `./bin/tailwindcss -i styling/static_src/input.css -o styling/static_src/output.css --watch`
- No Node.js, no `package.json`, no `django-tailwind` dependency

### Brand color tokens (in `input.css`)
```css
@import "tailwindcss";

@theme {
  --color-primary: #1a56a0;
  --color-secondary: #f5a623;
  --color-accent: #2d6a4f;
  --color-surface: #f9fafb;
}
```
Gives utilities: `bg-primary`, `text-secondary`, `border-accent` etc.

### Alpine.js usage
- Mobile nav: `x-data="{ open: false }"` on `<header>`
- FAQ accordion: `x-data="{ active: null }"` per item
- Gallery filter: `x-data="{ category: 'all' }"` on gallery container
- Testimonial carousel: `x-data="{ current: 0 }"` with prev/next buttons
- Toast notification: `x-data="{ show: false, message: '' }"`

---

## Settings Architecture

```
project/settings/
├── __init__.py       empty
├── base.py           INSTALLED_APPS, MIDDLEWARE, TEMPLATES, AUTH, i18n, logging
├── development.py    imports base; DEBUG=True, SQLite, console email, local media
└── production.py     imports base; reads .env, DATABASE_URL, STORAGE_BACKEND, SMTP
```

### Storage switching (`production.py`)
```python
STORAGE_BACKEND = env('STORAGE_BACKEND', default='local')

if STORAGE_BACKEND == 's3':
    STORAGES = {"default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"}}
elif STORAGE_BACKEND == 'gcs':
    STORAGES = {"default": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"}}
# else: Django default FileSystemStorage
```

### Database (`production.py`)
```python
DATABASES = {'default': dj_database_url.config(default=env('DATABASE_URL'))}
```
Supports MySQL (`mysql://`) and PostgreSQL (`postgresql://`). `mysqlclient` added to requirements.

---

## Deployment

### cPanel (primary target)
1. Upload project via Git or file manager
2. Create Python app in cPanel → points to `passenger_wsgi.py`
3. Set env vars in cPanel Python app environment panel
4. Run `python manage.py migrate && python manage.py collectstatic --noinput`
5. cPanel/Apache serves `/static/` and `/media/` from filesystem directly

**`passenger_wsgi.py`:**
```python
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.production')
from project.wsgi import application
```

### PaaS (Railway, Render, DigitalOcean)
Existing `Procfile` kept:
```
release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn project.wsgi:application
```
Set `DJANGO_SETTINGS_MODULE=project.settings.production` in platform env vars.

---

## `.env.example`

```bash
DJANGO_SETTINGS_MODULE=project.settings.production
SECRET_KEY=change-me
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
ALLOWED_CORS=https://yourdomain.com
DATABASE_URL=mysql://user:pass@localhost/dbname
STORAGE_BACKEND=local
EMAIL_HOST=smtpout.server.net
EMAIL_HOST_USER=info@yourdomain.com
EMAIL_HOST_PASSWORD=
GOOGLE_ANALYTICS=G-XXXXXXXXXX
```

---

## Requirements Changes

**Remove:**
- `google-cloud-storage`
- `google-api-python-client`
- `django-tailwind`
- `django-browser-reload`
- `firebase` / `google.oauth2` (from google-auth, transitive)

**Add:**
- `django==5.2`
- `mysqlclient`
- `boto3` + `django-storages[s3]` (optional cloud storage)

**Keep:**
- `django-environ`, `dj-database-url`, `whitenoise`, `gunicorn`
- `django-ratelimit`, `django-cors-headers`
- `djangorestframework-simplejwt`, `django-phonenumber-field`
- `pillow`, `psycopg2-binary`, `pytz`
- `django-cleanup`

---

## Data Migrations (pre-populated defaults)

`core` app ships one data migration that creates:
- `SiteConfig` row with placeholder values
- 10 `HomepageSection` rows (all active, default order: hero→about→services→team→events→gallery→testimonials→partners→news→faq)
- Default `NavLink` rows: Home(1), About(2), Events(3), Blog(4), Contact(5)
- Default `FooterLink` rows: Home(1), About(2), Contact(3), Privacy Policy(4)

---

## Out of Scope

- User registration / public accounts (admin access only)
- Newsletter backend (frontend form exists, backend integration left to buyer)
- Payment / membership fees
- Multi-language support
- Chess-specific features (rankings, player profiles, tournament brackets) — those are built on top of this template for the Uganda Chess Federation project specifically
