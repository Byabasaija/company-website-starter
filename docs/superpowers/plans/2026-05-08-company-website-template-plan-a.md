# Company Website Template — Plan A: Foundation + Core App

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the Django starter to 5.2 LTS, replace Tailwind setup with v4 standalone CLI + Alpine.js, strip Firebase dependency, split settings for cPanel deployment, and build the `core` app that drives all homepage content from Django admin.

**Architecture:** The `core` app owns a `SiteConfig` singleton (branding), `HomepageSection` (ordered, togglable section list), and all homepage section content models. A context processor injects `site`, `nav_links`, and `footer_links` into every template. The home view assembles the page by iterating active `HomepageSection` rows and including the matching section partial.

**Tech Stack:** Django 5.2 LTS, Tailwind CSS v4 standalone CLI, Alpine.js 3 (CDN), Bootstrap Icons (CDN), SQLite (dev) / MySQL or PostgreSQL (prod via DATABASE_URL), Whitenoise (static, non-cPanel), Passenger WSGI (cPanel).

**Spec:** `docs/superpowers/specs/2026-05-08-company-website-template-design.md`

**Plan B:** `docs/superpowers/plans/2026-05-08-company-website-template-plan-b.md` (Events, Gallery, FAQ, full frontend polish — write after this plan ships)

---

## File Map

### Created
```
passenger_wsgi.py
.env.example
bin/.gitkeep                              (directory for tailwindcss binary)
project/settings/__init__.py
project/settings/base.py
project/settings/development.py
project/settings/production.py
core/__init__.py
core/apps.py
core/models.py
core/admin.py
core/views.py
core/urls.py
core/context_processors.py
core/migrations/0001_initial.py           (auto-generated)
core/migrations/0002_default_data.py      (hand-written data migration)
tests/__init__.py
tests/test_core_models.py
tests/test_core_views.py
styling/static_src/input.css              (Tailwind v4 source)
styling/static_src/output.css             (compiled, committed)
templates/html/base.html                  (full rewrite)
templates/html/home.html                  (full rewrite)
templates/html/components/sections/hero.html
templates/html/components/sections/about.html
templates/html/components/sections/services.html
templates/html/components/sections/team.html
templates/html/components/sections/testimonials.html
templates/html/components/sections/partners.html
templates/html/components/sections/latest-news.html
templates/html/components/sections/upcoming-events.html   (stub)
templates/html/components/sections/gallery-preview.html   (stub)
templates/html/components/sections/faq-preview.html       (stub)
templates/html/about.html
templates/html/services.html
```

### Modified
```
requirements.txt
project/urls.py
project/wsgi.py
.gitignore
Procfile
inquiry/urls.py
```

### Deleted
```
project/settings.py              (replaced by project/settings/ package)
build_files.sh                   (Firebase-specific build script)
styling/static_src/package.json
styling/static_src/package-lock.json
styling/static_src/tailwind.config.js
styling/static_src/postcss.config.js
```

---

## Task 1: Upgrade dependencies

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Write new requirements.txt**

```
django==5.2
django-environ==0.11.2
django-cleanup==8.1.0
psycopg2-binary==2.9.9
mysqlclient==2.2.4
django-storages==1.14.4
boto3==1.35.0
django-cors-headers==4.3.1
django-ratelimit==4.1.0
dj-database-url==2.2.0
djangorestframework-simplejwt==5.3.1
pytz==2024.1
django-phonenumber-field[phonenumberslite]==7.3.0
whitenoise==6.7.0
pillow==10.4.0
gunicorn==22.0.0
```

- [ ] **Step 2: Install and verify**

```bash
pip install -r requirements.txt
python -c "import django; print(django.__version__)"
```
Expected: `5.2`

- [ ] **Step 3: Delete removed files**

```bash
rm -f build_files.sh
rm -f styling/static_src/package.json
rm -f styling/static_src/package-lock.json
rm -f styling/static_src/tailwind.config.js
rm -f styling/static_src/postcss.config.js
```

- [ ] **Step 4: Commit**

```bash
git add requirements.txt
git rm --cached build_files.sh styling/static_src/package.json styling/static_src/package-lock.json styling/static_src/tailwind.config.js styling/static_src/postcss.config.js 2>/dev/null || true
git rm build_files.sh styling/static_src/package.json styling/static_src/package-lock.json styling/static_src/tailwind.config.js styling/static_src/postcss.config.js 2>/dev/null || true
git commit -m "chore: upgrade to Django 5.2, remove Firebase/django-tailwind deps"
```

---

## Task 2: Split settings

**Files:**
- Create: `project/settings/__init__.py`
- Create: `project/settings/base.py`
- Create: `project/settings/development.py`
- Create: `project/settings/production.py`
- Delete: `project/settings.py`

- [ ] **Step 1: Create the settings package**

```bash
mkdir -p project/settings
touch project/settings/__init__.py
```

- [ ] **Step 2: Create `project/settings/base.py`**

```python
import os
from pathlib import Path
import environ

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-me-in-production')

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # 3rd party
    'corsheaders',
    'django_cleanup.apps.CleanupConfig',

    # first party
    'core',
    'user',
    'blog',
    'inquiry',
]

SITE_ID = 1
AUTH_USER_MODEL = 'user.User'
LOGIN_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_ratelimit.middleware.RatelimitMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates' / 'html',
            BASE_DIR / 'templates' / 'html' / 'error',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_config',
            ],
            'libraries': {
                'custom_tags': 'project.templatetags.custom_tags',
            },
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' / 'static'
STATICFILES_DIRS = [BASE_DIR / 'templates']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

- [ ] **Step 3: Create `project/settings/development.py`**

```python
import environ
from .base import *

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env.local')

DEBUG = True
SECRET_KEY = env('SECRET_KEY', default='django-insecure-dev-only-key')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

INSTALLED_APPS += ['django_browser_reload']
MIDDLEWARE += ['django_browser_reload.middleware.BrowserReloadMiddleware']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

GOOGLE_ANALYTICS = env('GOOGLE_ANALYTICS', default='')

INTERNAL_IPS = ['127.0.0.1']
```

- [ ] **Step 4: Create `project/settings/production.py`**

```python
import environ
import dj_database_url
from .base import *

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = False
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env('ALLOWED_HOSTS').replace(' ', '').split(',')
CORS_ALLOWED_ORIGINS = env('ALLOWED_CORS', default='').replace(' ', '').split(',')
CSRF_TRUSTED_ORIGINS = env('ALLOWED_CORS', default='').replace(' ', '').split(',')

DATABASES = {'default': dj_database_url.config(default=env('DATABASE_URL'))}

GOOGLE_ANALYTICS = env('GOOGLE_ANALYTICS', default='')

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default=465)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Storage
STORAGE_BACKEND = env('STORAGE_BACKEND', default='local')

if STORAGE_BACKEND == 's3':
    STORAGES = {
        'default': {'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
    }
    AWS_STORAGE_BUCKET_NAME = env('AWS_BUCKET_NAME')
    AWS_S3_REGION_NAME = env('AWS_REGION', default='us-east-1')
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
elif STORAGE_BACKEND == 'gcs':
    from google.oauth2 import service_account
    STORAGES = {
        'default': {'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
    }
    GS_BUCKET_NAME = env('GCS_BUCKET_NAME')
    GS_PROJECT_ID = env('GCS_PROJECT_ID')
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        BASE_DIR / env('GCS_CRED_PATH')
    )
# else: Django default FileSystemStorage — works on cPanel
```

- [ ] **Step 5: Update `project/wsgi.py` default settings module**

Replace the `os.environ.setdefault` line:
```python
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.development')
application = get_wsgi_application()
```

- [ ] **Step 6: Delete old settings file**

```bash
git rm project/settings.py
```

- [ ] **Step 7: Also add `django_browser_reload` to requirements for dev**

Append to `requirements.txt`:
```
django-browser-reload==1.13.0
```

Then re-run `pip install -r requirements.txt`.

- [ ] **Step 8: Verify Django starts**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py check
```
Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 9: Commit**

```bash
git add project/settings/ project/wsgi.py requirements.txt
git commit -m "chore: split settings into base/development/production"
```

---

## Task 3: Tailwind v4 standalone CLI

**Files:**
- Create: `bin/.gitkeep`
- Modify: `.gitignore`
- Create: `styling/static_src/input.css`
- Create: `styling/static_src/output.css`

- [ ] **Step 1: Add `bin/` to .gitignore (binary), keep directory**

```bash
mkdir -p bin
touch bin/.gitkeep
```

Add to `.gitignore`:
```
# Tailwind standalone binary
bin/tailwindcss
bin/tailwindcss.exe
```

- [ ] **Step 2: Download the Tailwind v4 standalone binary**

On macOS Apple Silicon:
```bash
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64
mv tailwindcss-macos-arm64 bin/tailwindcss
chmod +x bin/tailwindcss
```

On macOS Intel:
```bash
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-x64
mv tailwindcss-macos-x64 bin/tailwindcss
chmod +x bin/tailwindcss
```

On Linux (for cPanel server reference — run on the server, not committed):
```bash
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
mv tailwindcss-linux-x64 bin/tailwindcss
chmod +x bin/tailwindcss
```

- [ ] **Step 3: Create `styling/static_src/input.css`**

```css
@import "tailwindcss";

@source "../../templates/**/*.html";
@source "../../templates/**/*.js";
@source "../../**/templates/**/*.html";

@theme {
  --color-primary: #1a56a0;
  --color-secondary: #f5a623;
  --color-accent: #2d6a4f;
  --color-surface: #f9fafb;

  --font-sans: 'Inter', ui-sans-serif, system-ui, sans-serif;
}

/* Base component styles */
@layer components {
  .btn-primary {
    @apply bg-primary text-white px-6 py-2 rounded-lg font-medium hover:bg-primary/90 transition-colors;
  }
  .btn-outline {
    @apply border border-primary text-primary px-6 py-2 rounded-lg font-medium hover:bg-primary hover:text-white transition-colors;
  }
  .section-padding {
    @apply px-6 lg:px-16 py-16;
  }
  .section-title {
    @apply text-3xl lg:text-4xl font-bold text-gray-900 mb-4;
  }
  .section-subtitle {
    @apply text-lg text-gray-600 mb-10;
  }
  .card {
    @apply bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden;
  }
  .input {
    @apply w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary;
  }
}
```

- [ ] **Step 4: Compile initial output.css**

```bash
./bin/tailwindcss -i styling/static_src/input.css -o templates/css/output.css --minify
```
Expected: `Done in Xms.` — creates `templates/css/output.css`.

- [ ] **Step 5: Verify output exists**

```bash
wc -l templates/css/output.css
```
Expected: a single minified line (or a few lines).

- [ ] **Step 6: Commit**

```bash
git add bin/.gitkeep .gitignore styling/static_src/input.css templates/css/output.css
git commit -m "chore: add Tailwind v4 standalone CLI setup"
```

---

## Task 4: cPanel deployment files

**Files:**
- Create: `passenger_wsgi.py`
- Create: `.env.example`
- Modify: `Procfile`

- [ ] **Step 1: Create `passenger_wsgi.py`**

```python
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.production')

from project.wsgi import application
```

- [ ] **Step 2: Create `.env.example`**

```bash
# Copy this to .env (production) or .env.local (development) and fill in values.

# Settings module
DJANGO_SETTINGS_MODULE=project.settings.production

# Security
SECRET_KEY=change-this-to-a-long-random-string

# Hosts
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
ALLOWED_CORS=https://yourdomain.com,https://www.yourdomain.com

# Database — cPanel MySQL or PostgreSQL
# MySQL:      mysql://user:password@localhost/dbname
# PostgreSQL: postgresql://user:password@localhost/dbname
DATABASE_URL=mysql://user:password@localhost/dbname

# File storage: local (default, works on cPanel), s3, or gcs
STORAGE_BACKEND=local

# Email (cPanel SMTP or any provider)
EMAIL_HOST=smtpout.secureserver.net
EMAIL_PORT=465
EMAIL_HOST_USER=info@yourdomain.com
EMAIL_HOST_PASSWORD=

# Optional — Google Analytics measurement ID
GOOGLE_ANALYTICS=G-XXXXXXXXXX

# Optional — S3 storage (only if STORAGE_BACKEND=s3)
# AWS_BUCKET_NAME=
# AWS_REGION=us-east-1
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
```

- [ ] **Step 3: Update Procfile for PaaS (non-cPanel)**

```
release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn project.wsgi:application --workers 2 --bind 0.0.0.0:$PORT
```

- [ ] **Step 4: Add `.env` to .gitignore (keep `.env.local` entry already there)**

Verify `.gitignore` contains:
```
.env
.env.local
*.pyc
__pycache__/
db.sqlite3
media/
staticfiles/
bin/tailwindcss
bin/tailwindcss.exe
```

Add any missing lines.

- [ ] **Step 5: Verify passenger_wsgi imports cleanly**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python -c "import passenger_wsgi; print('OK')"
```
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add passenger_wsgi.py .env.example Procfile .gitignore
git commit -m "chore: add cPanel passenger_wsgi, .env.example, update Procfile"
```

---

## Task 5: Create `core` app — SiteConfig + HomepageSection

**Files:**
- Create: `core/__init__.py`, `core/apps.py`, `core/models.py` (partial), `core/migrations/0001_initial.py` (auto)
- Create: `tests/__init__.py`, `tests/test_core_models.py`

- [ ] **Step 1: Create the app**

```bash
python manage.py startapp core
```

- [ ] **Step 2: Write `core/apps.py`**

```python
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
```

- [ ] **Step 3: Write failing tests first**

Create `tests/__init__.py` (empty) and `tests/test_core_models.py`:

```python
from django.test import TestCase
from core.models import SiteConfig, HomepageSection


class SiteConfigSingletonTest(TestCase):

    def test_save_always_uses_pk_1(self):
        config = SiteConfig(site_name='Test Site')
        config.save()
        self.assertEqual(config.pk, 1)

    def test_second_save_overwrites_not_creates(self):
        SiteConfig(site_name='First').save()
        SiteConfig(site_name='Second').save()
        self.assertEqual(SiteConfig.objects.count(), 1)
        self.assertEqual(SiteConfig.objects.get(pk=1).site_name, 'Second')


class HomepageSectionOrderingTest(TestCase):

    def test_sections_ordered_by_order_field(self):
        HomepageSection.objects.create(section_type='about', order=2, is_active=True)
        HomepageSection.objects.create(section_type='hero', order=1, is_active=True)
        sections = list(HomepageSection.objects.all())
        self.assertEqual(sections[0].section_type, 'hero')
        self.assertEqual(sections[1].section_type, 'about')

    def test_inactive_sections_excluded_when_filtered(self):
        HomepageSection.objects.create(section_type='hero', order=1, is_active=True)
        HomepageSection.objects.create(section_type='about', order=2, is_active=False)
        active = HomepageSection.objects.filter(is_active=True)
        self.assertEqual(active.count(), 1)
        self.assertEqual(active.first().section_type, 'hero')
```

- [ ] **Step 4: Run tests — expect failure (models don't exist yet)**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_core_models -v 2
```
Expected: `ImportError: cannot import name 'SiteConfig' from 'core.models'`

- [ ] **Step 5: Write `core/models.py` — SiteConfig and HomepageSection only**

```python
from django.db import models


class SiteConfig(models.Model):
    site_name       = models.CharField(max_length=100, default='My Company')
    tagline         = models.CharField(max_length=200, blank=True)
    logo            = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon         = models.ImageField(upload_to='site/', blank=True, null=True)
    primary_color   = models.CharField(max_length=7, default='#1a56a0')
    secondary_color = models.CharField(max_length=7, default='#f5a623')
    email           = models.EmailField(blank=True)
    phone           = models.CharField(max_length=20, blank=True)
    address         = models.TextField(blank=True)
    footer_text     = models.CharField(max_length=200, blank=True)
    facebook        = models.URLField(blank=True)
    twitter         = models.URLField(blank=True)
    instagram       = models.URLField(blank=True)
    linkedin        = models.URLField(blank=True)
    youtube         = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Site Configuration'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class HomepageSection(models.Model):
    SECTION_TYPES = [
        ('hero',         'Hero Banner'),
        ('about',        'About Us'),
        ('services',     'Services / Programs'),
        ('team',         'Our Team'),
        ('events',       'Upcoming Events'),
        ('gallery',      'Photo Gallery'),
        ('testimonials', 'Testimonials'),
        ('partners',     'Partners & Sponsors'),
        ('news',         'Latest News / Blog'),
        ('faq',          'FAQ'),
    ]
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES, unique=True)
    order        = models.PositiveIntegerField(default=0)
    is_active    = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.get_section_type_display()} (order: {self.order})'
```

- [ ] **Step 6: Add `core` to INSTALLED_APPS in `project/settings/base.py`**

Verify `'core'` is in `INSTALLED_APPS` (it was included in Task 2 — check it's there).

- [ ] **Step 7: Run migrations**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py makemigrations core
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py migrate
```
Expected: migrations created and applied cleanly.

- [ ] **Step 8: Run tests — expect pass**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_core_models -v 2
```
Expected: `Ran 4 tests ... OK`

- [ ] **Step 9: Commit**

```bash
git add core/ tests/ project/settings/base.py
git commit -m "feat: add core app with SiteConfig singleton and HomepageSection models"
```

---

## Task 6: Add section content models to `core`

**Files:**
- Modify: `core/models.py` (append HeroSection, AboutSection, TeamMember, Service, Testimonial, Partner)
- Create: `core/migrations/0002_section_models.py` (auto-generated)

- [ ] **Step 1: Write failing tests**

Append to `tests/test_core_models.py`:

```python
from core.models import HeroSection, AboutSection, TeamMember, Service, Testimonial, Partner


class HeroSectionTest(TestCase):
    def test_create_hero(self):
        hero = HeroSection.objects.create(
            headline='Welcome',
            subheadline='We are here',
            cta_text='Learn more',
            cta_url='/about/',
        )
        self.assertEqual(HeroSection.objects.count(), 1)
        self.assertEqual(hero.headline, 'Welcome')


class TeamMemberTest(TestCase):
    def test_team_members_ordered_by_order_field(self):
        TeamMember.objects.create(name='Bob', role='CEO', order=2, is_active=True)
        TeamMember.objects.create(name='Alice', role='CTO', order=1, is_active=True)
        members = list(TeamMember.objects.filter(is_active=True))
        self.assertEqual(members[0].name, 'Alice')

    def test_inactive_members_excluded(self):
        TeamMember.objects.create(name='Active', role='CEO', order=1, is_active=True)
        TeamMember.objects.create(name='Inactive', role='CFO', order=2, is_active=False)
        self.assertEqual(TeamMember.objects.filter(is_active=True).count(), 1)
```

- [ ] **Step 2: Run tests — expect failure**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_core_models -v 2
```
Expected: `ImportError: cannot import name 'HeroSection'`

- [ ] **Step 3: Append section models to `core/models.py`**

Add after the `HomepageSection` class:

```python
class HeroSection(models.Model):
    headline     = models.CharField(max_length=200, default='Welcome')
    subheadline  = models.CharField(max_length=300, blank=True)
    cta_text     = models.CharField(max_length=50, default='Learn More')
    cta_url      = models.CharField(max_length=200, default='/about/')
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)

    class Meta:
        verbose_name = 'Hero Section'

    def __str__(self):
        return self.headline


class AboutSection(models.Model):
    heading = models.CharField(max_length=200, default='About Us')
    body    = models.TextField(blank=True)
    image   = models.ImageField(upload_to='about/', blank=True, null=True)

    class Meta:
        verbose_name = 'About Section'

    def __str__(self):
        return self.heading


class TeamMember(models.Model):
    name      = models.CharField(max_length=100)
    role      = models.CharField(max_length=100)
    photo     = models.ImageField(upload_to='team/', blank=True, null=True)
    bio       = models.TextField(blank=True)
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    facebook  = models.URLField(blank=True)
    twitter   = models.URLField(blank=True)
    linkedin  = models.URLField(blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} — {self.role}'


class Service(models.Model):
    title       = models.CharField(max_length=100)
    description = models.TextField()
    icon        = models.CharField(max_length=50, default='bi-star', help_text='Bootstrap icon name e.g. bi-trophy')
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name         = models.CharField(max_length=100)
    role         = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    quote        = models.TextField()
    photo        = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    order        = models.PositiveIntegerField(default=0)
    is_active    = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} — {self.organization}'


class Partner(models.Model):
    name        = models.CharField(max_length=100)
    logo        = models.ImageField(upload_to='partners/')
    website_url = models.URLField(blank=True)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
```

- [ ] **Step 4: Create and run migrations**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py makemigrations core
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py migrate
```

- [ ] **Step 5: Run all tests — expect pass**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_core_models -v 2
```
Expected: `Ran 7 tests ... OK`

- [ ] **Step 6: Commit**

```bash
git add core/models.py core/migrations/ tests/test_core_models.py
git commit -m "feat: add HeroSection, AboutSection, TeamMember, Service, Testimonial, Partner models"
```

---

## Task 7: NavLink, FooterLink models + data migration

**Files:**
- Modify: `core/models.py` (append NavLink, FooterLink)
- Create: `core/migrations/0003_nav_footer_links.py` (auto)
- Create: `core/migrations/0004_default_data.py` (hand-written)

- [ ] **Step 1: Write failing tests**

Append to `tests/test_core_models.py`:

```python
from core.models import NavLink, FooterLink


class NavLinkTest(TestCase):
    def test_active_links_ordered(self):
        NavLink.objects.create(label='Contact', url='/contact/', order=3, is_active=True)
        NavLink.objects.create(label='Home', url='/', order=1, is_active=True)
        NavLink.objects.create(label='Hidden', url='/hidden/', order=2, is_active=False)
        active = list(NavLink.objects.filter(is_active=True))
        self.assertEqual(len(active), 2)
        self.assertEqual(active[0].label, 'Home')
        self.assertEqual(active[1].label, 'Contact')
```

- [ ] **Step 2: Run tests — expect failure**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_core_models -v 2
```
Expected: `ImportError: cannot import name 'NavLink'`

- [ ] **Step 3: Append to `core/models.py`**

```python
class NavLink(models.Model):
    label     = models.CharField(max_length=50)
    url       = models.CharField(max_length=200)
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label


class FooterLink(models.Model):
    label     = models.CharField(max_length=50)
    url       = models.CharField(max_length=200)
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label
```

- [ ] **Step 4: Generate migrations**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py makemigrations core
```

- [ ] **Step 5: Write the data migration**

Create `core/migrations/0004_default_data.py`:

```python
from django.db import migrations


def create_defaults(apps, schema_editor):
    SiteConfig = apps.get_model('core', 'SiteConfig')
    HomepageSection = apps.get_model('core', 'HomepageSection')
    NavLink = apps.get_model('core', 'NavLink')
    FooterLink = apps.get_model('core', 'FooterLink')
    HeroSection = apps.get_model('core', 'HeroSection')
    AboutSection = apps.get_model('core', 'AboutSection')

    SiteConfig.objects.get_or_create(pk=1, defaults={
        'site_name': 'My Company',
        'tagline': 'Your tagline here',
        'primary_color': '#1a56a0',
        'secondary_color': '#f5a623',
        'footer_text': '© 2026 My Company. All rights reserved.',
    })

    sections = [
        ('hero',         1),
        ('about',        2),
        ('services',     3),
        ('team',         4),
        ('events',       5),
        ('gallery',      6),
        ('testimonials', 7),
        ('partners',     8),
        ('news',         9),
        ('faq',         10),
    ]
    for section_type, order in sections:
        HomepageSection.objects.get_or_create(
            section_type=section_type,
            defaults={'order': order, 'is_active': True},
        )

    nav_defaults = [
        ('Home',     '/',         1),
        ('About',    '/about/',   2),
        ('Blog',     '/blog/',    3),
        ('Contact',  '/contact/', 4),
    ]
    for label, url, order in nav_defaults:
        NavLink.objects.get_or_create(label=label, defaults={'url': url, 'order': order, 'is_active': True})

    footer_defaults = [
        ('Home',           '/',               1),
        ('About',          '/about/',         2),
        ('Contact',        '/contact/',       3),
        ('Privacy Policy', '/privacy/',       4),
    ]
    for label, url, order in footer_defaults:
        FooterLink.objects.get_or_create(label=label, defaults={'url': url, 'order': order, 'is_active': True})

    HeroSection.objects.get_or_create(pk=1, defaults={
        'headline': 'Welcome to Our Organisation',
        'subheadline': 'Empowering communities through excellence.',
        'cta_text': 'Learn More',
        'cta_url': '/about/',
    })

    AboutSection.objects.get_or_create(pk=1, defaults={
        'heading': 'About Us',
        'body': 'We are a dedicated organisation committed to our mission.',
    })


def reverse_defaults(apps, schema_editor):
    pass  # leave data in place on reverse


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_nav_footer_links'),
    ]
    operations = [
        migrations.RunPython(create_defaults, reverse_defaults),
    ]
```

- [ ] **Step 6: Run all migrations**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py migrate
```
Expected: migrations apply cleanly, default data created.

- [ ] **Step 7: Run all tests**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_core_models -v 2
```
Expected: `Ran 8 tests ... OK`

- [ ] **Step 8: Commit**

```bash
git add core/models.py core/migrations/
git commit -m "feat: add NavLink, FooterLink models and default data migration"
```

---

## Task 8: Core admin

**Files:**
- Create: `core/admin.py`

- [ ] **Step 1: Write `core/admin.py`**

```python
from django.contrib import admin
from .models import (SiteConfig, HomepageSection, HeroSection, AboutSection,
                     TeamMember, Service, Testimonial, Partner, NavLink, FooterLink)


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identity', {'fields': ('site_name', 'tagline', 'logo', 'favicon')}),
        ('Brand Colors', {'fields': ('primary_color', 'secondary_color')}),
        ('Contact', {'fields': ('email', 'phone', 'address')}),
        ('Social Links', {'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'youtube')}),
        ('Footer', {'fields': ('footer_text',)}),
    )

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomepageSection)
class HomepageSectionAdmin(admin.ModelAdmin):
    list_display  = ('get_section_type_display', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering      = ('order',)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    pass


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    pass


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display  = ('name', 'role', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ('title', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ('name', 'organization', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display  = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(NavLink)
class NavLinkAdmin(admin.ModelAdmin):
    list_display  = ('label', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display  = ('label', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
```

- [ ] **Step 2: Verify admin loads**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py check
```
Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 3: Create superuser and verify in browser**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py createsuperuser
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py runserver
```
Open `http://127.0.0.1:8000/admin/` — verify all core models appear, SiteConfig shows as a change form (no Add button), HomepageSection list has inline editable order/active fields.

- [ ] **Step 4: Commit**

```bash
git add core/admin.py
git commit -m "feat: add core admin with SiteConfig singleton enforcement"
```

---

## Task 9: Context processor + URL wiring

**Files:**
- Create: `core/context_processors.py`
- Create: `core/views.py`
- Create: `core/urls.py`
- Modify: `project/urls.py`
- Modify: `inquiry/urls.py` (rename `/contact-us/` → `/contact/`)

- [ ] **Step 1: Write failing view test**

Create `tests/test_core_views.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from core.models import SiteConfig, HomepageSection, HeroSection, AboutSection


class HomepageViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        SiteConfig(site_name='Test Site').save()
        HomepageSection.objects.create(section_type='hero', order=1, is_active=True)
        HomepageSection.objects.create(section_type='about', order=2, is_active=False)
        HeroSection.objects.create(headline='Hello', cta_text='Go', cta_url='/')
        AboutSection.objects.create(heading='About', body='We exist.')

    def test_homepage_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_context_has_site(self):
        response = self.client.get('/')
        self.assertIn('site', response.context)
        self.assertEqual(response.context['site'].site_name, 'Test Site')

    def test_homepage_context_has_active_sections(self):
        response = self.client.get('/')
        sections = list(response.context['homepage_sections'])
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].section_type, 'hero')

    def test_about_page_returns_200(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_services_page_returns_200(self):
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)
```

- [ ] **Step 2: Run test — expect failure (no URLs yet)**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_core_views -v 2
```
Expected: `404` errors or `NoReverseMatch`.

- [ ] **Step 3: Write `core/context_processors.py`**

```python
from .models import SiteConfig, NavLink, FooterLink


def site_config(request):
    try:
        site = SiteConfig.objects.get(pk=1)
    except SiteConfig.DoesNotExist:
        site = SiteConfig(site_name='My Company')

    return {
        'site': site,
        'nav_links': NavLink.objects.filter(is_active=True),
        'footer_links': FooterLink.objects.filter(is_active=True),
    }
```

- [ ] **Step 4: Write `core/views.py`**

```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import (HomepageSection, HeroSection, AboutSection,
                     TeamMember, Service, Testimonial, Partner)
from blog.models import Blog


def home_view(request):
    context = {
        'homepage_sections': HomepageSection.objects.filter(is_active=True),
        'hero':         HeroSection.objects.first(),
        'about':        AboutSection.objects.first(),
        'team_members': TeamMember.objects.filter(is_active=True),
        'services':     Service.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True),
        'partners':     Partner.objects.filter(is_active=True),
        'latest_blogs': Blog.objects.filter(draft=False).order_by('-datetime')[:3],
        # Stubs — filled in Plan B when events/gallery/faq apps are added
        'upcoming_events': [],
        'gallery_images':  [],
        'faq_items':       [],
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
    return redirect('/about/')
```

- [ ] **Step 5: Write `core/urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('',         views.home_view,    name='home'),
    path('about/',   views.about_view,   name='about'),
    path('team/',    views.team_redirect, name='team'),
    path('services/', views.services_view, name='services'),
]
```

- [ ] **Step 6: Rewrite `project/urls.py`**

```python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.shortcuts import render

from project.sitemaps import StaticSitemap
from blog.sitemaps import BlogSitemap

admin.site.site_header = 'Site Admin'
admin.site.index_title = 'Dashboard'
admin.site.site_title = 'Admin'
admin.site.site_url = '/'

sitemap_dict = {'sitemaps': {'static': StaticSitemap, 'blog': BlogSitemap}}


def rate_limiter_view(request, *args, **kwargs):
    return render(request, 'ratelimit.html', status=429)


def view_404(request, *args, **kwargs):
    return render(request, '404.html', status=404)


handler404 = view_404

urlpatterns = [
    path('admin/',       admin.site.urls),
    path('',             include('core.urls')),
    path('blog/',        include('blog.urls')),
    path('contact/',     include('inquiry.urls')),

    path('sitemap.xml',  sitemap, sitemap_dict, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt',   TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('ratelimit-error/', rate_limiter_view, name='ratelimit-error'),
]

if settings.DEBUG:
    urlpatterns += [path('__reload__/', include('django_browser_reload.urls'))]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [re_path(r'^.*/$', view_404, name='page_not_found')]
```

- [ ] **Step 7: Update `inquiry/urls.py` — fix contact success URL name**

```python
from django.urls import path
from .views import inquiry_create_view, inquiry_success_view

urlpatterns = [
    path('',         inquiry_create_view, name='contact-us'),
    path('success/', inquiry_success_view, name='contact-success'),
]
```

Note: verify `inquiry/views.py` has `inquiry_success_view` — if not, add it:

```python
def inquiry_success_view(request):
    return render(request, 'html/components/pages/success.html')
```

- [ ] **Step 8: Run view tests**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests.test_core_views -v 2
```
Expected: `Ran 5 tests ... OK` (templates don't exist yet — these will fail until Task 10. If they fail with `TemplateDoesNotExist`, that's expected and fine — the URL routing works.)

Actually: Django test client will raise `TemplateDoesNotExist`. Create minimal stub templates to let the tests pass:

```bash
mkdir -p templates/html
echo "{% block content %}{% endblock %}" > templates/html/home.html
echo "{% block content %}{% endblock %}" > templates/html/about.html
echo "{% block content %}{% endblock %}" > templates/html/services.html
```

Then re-run — expected: `Ran 5 tests ... OK`.

- [ ] **Step 9: Run all tests**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests -v 2
```
Expected: all tests pass.

- [ ] **Step 10: Commit**

```bash
git add core/ project/urls.py inquiry/urls.py inquiry/views.py templates/html/home.html templates/html/about.html templates/html/services.html
git commit -m "feat: add context processor, core views, URL routing"
```

---

## Task 10: Rewrite base.html

**Files:**
- Modify: `templates/html/base.html` (full rewrite)

- [ ] **Step 1: Rewrite `templates/html/base.html`**

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %} | {{ site.site_name }}</title>
    <meta name="description" content="{% block description %}{{ site.tagline }}{% endblock %}">

    {% if site.favicon %}<link rel="icon" href="{{ site.favicon.url }}">{% endif %}

    <!-- Open Graph -->
    <meta property="og:title" content="{% block og_title %}{{ site.site_name }}{% endblock %}">
    <meta property="og:description" content="{% block og_description %}{{ site.tagline }}{% endblock %}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{{ request.build_absolute_uri }}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">

    <!-- Styles -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
    <link rel="stylesheet" href="{% static 'css/output.css' %}">

    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.1/dist/cdn.min.js"></script>

    {% if GOOGLE_ANALYTICS %}
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ GOOGLE_ANALYTICS }}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '{{ GOOGLE_ANALYTICS }}');
    </script>
    {% endif %}

    {% block head %}{% endblock %}
</head>

<body class="min-h-screen flex flex-col bg-white text-gray-900">

    <!-- Navbar -->
    <header x-data="{ open: false }"
            class="w-full h-16 fixed top-0 z-50 bg-white border-b border-gray-100 shadow-sm">
        <div class="max-w-7xl mx-auto px-6 lg:px-8 h-full flex items-center justify-between">

            <!-- Logo -->
            <a href="/" class="flex items-center gap-3 shrink-0">
                {% if site.logo %}
                    <img src="{{ site.logo.url }}" alt="{{ site.site_name }}"
                         class="h-10 w-auto object-contain">
                {% else %}
                    <span class="text-xl font-bold text-primary">{{ site.site_name }}</span>
                {% endif %}
            </a>

            <!-- Desktop nav -->
            <nav class="hidden lg:flex items-center gap-8 text-sm font-medium">
                {% for link in nav_links %}
                    <a href="{{ link.url }}"
                       class="text-gray-600 hover:text-primary transition-colors duration-200">
                        {{ link.label }}
                    </a>
                {% endfor %}
            </nav>

            <!-- Desktop social icons -->
            <div class="hidden lg:flex items-center gap-4 text-lg text-gray-500">
                {% if site.facebook %}
                    <a href="{{ site.facebook }}" target="_blank" rel="noopener noreferrer"
                       aria-label="Facebook" class="hover:text-primary transition-colors">
                        <i class="bi bi-facebook"></i>
                    </a>
                {% endif %}
                {% if site.twitter %}
                    <a href="{{ site.twitter }}" target="_blank" rel="noopener noreferrer"
                       aria-label="Twitter" class="hover:text-primary transition-colors">
                        <i class="bi bi-twitter-x"></i>
                    </a>
                {% endif %}
                {% if site.instagram %}
                    <a href="{{ site.instagram }}" target="_blank" rel="noopener noreferrer"
                       aria-label="Instagram" class="hover:text-primary transition-colors">
                        <i class="bi bi-instagram"></i>
                    </a>
                {% endif %}
            </div>

            <!-- Mobile hamburger -->
            <button @click="open = !open"
                    class="lg:hidden p-2 text-2xl text-gray-700"
                    aria-label="Toggle menu">
                <i class="bi" :class="open ? 'bi-x' : 'bi-list'"></i>
            </button>
        </div>

        <!-- Mobile menu -->
        <div x-show="open"
             x-transition:enter="transition ease-out duration-200"
             x-transition:enter-start="opacity-0 -translate-y-2"
             x-transition:enter-end="opacity-100 translate-y-0"
             x-transition:leave="transition ease-in duration-150"
             x-transition:leave-end="opacity-0 -translate-y-2"
             class="lg:hidden absolute top-16 left-0 w-full bg-white border-b border-gray-100 shadow-md">
            <div class="px-6 py-4 flex flex-col gap-1">
                {% for link in nav_links %}
                    <a href="{{ link.url }}"
                       class="py-3 px-2 text-gray-700 hover:text-primary border-b border-gray-50 font-medium">
                        {{ link.label }}
                    </a>
                {% endfor %}
            </div>
        </div>
    </header>

    <!-- Main content -->
    <main class="mt-16 flex-1">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-400 mt-auto">
        <div class="max-w-7xl mx-auto px-6 lg:px-8 py-14 grid grid-cols-1 md:grid-cols-3 gap-10">

            <!-- Col 1: Brand -->
            <div class="flex flex-col gap-4">
                {% if site.logo %}
                    <img src="{{ site.logo.url }}" alt="{{ site.site_name }}"
                         class="h-10 w-auto object-contain brightness-0 invert">
                {% else %}
                    <span class="text-xl font-bold text-white">{{ site.site_name }}</span>
                {% endif %}
                {% if site.tagline %}
                    <p class="text-sm leading-relaxed">{{ site.tagline }}</p>
                {% endif %}
                {% if site.address %}
                    <p class="text-sm">{{ site.address }}</p>
                {% endif %}
                {% if site.email %}
                    <a href="mailto:{{ site.email }}" class="text-sm hover:text-white">{{ site.email }}</a>
                {% endif %}
                {% if site.phone %}
                    <p class="text-sm">{{ site.phone }}</p>
                {% endif %}

                <!-- Social -->
                <div class="flex gap-4 text-xl mt-2">
                    {% if site.facebook %}
                        <a href="{{ site.facebook }}" target="_blank" rel="noopener noreferrer"
                           aria-label="Facebook" class="hover:text-white transition-colors">
                            <i class="bi bi-facebook"></i>
                        </a>
                    {% endif %}
                    {% if site.twitter %}
                        <a href="{{ site.twitter }}" target="_blank" rel="noopener noreferrer"
                           aria-label="Twitter" class="hover:text-white transition-colors">
                            <i class="bi bi-twitter-x"></i>
                        </a>
                    {% endif %}
                    {% if site.instagram %}
                        <a href="{{ site.instagram }}" target="_blank" rel="noopener noreferrer"
                           aria-label="Instagram" class="hover:text-white transition-colors">
                            <i class="bi bi-instagram"></i>
                        </a>
                    {% endif %}
                    {% if site.linkedin %}
                        <a href="{{ site.linkedin }}" target="_blank" rel="noopener noreferrer"
                           aria-label="LinkedIn" class="hover:text-white transition-colors">
                            <i class="bi bi-linkedin"></i>
                        </a>
                    {% endif %}
                    {% if site.youtube %}
                        <a href="{{ site.youtube }}" target="_blank" rel="noopener noreferrer"
                           aria-label="YouTube" class="hover:text-white transition-colors">
                            <i class="bi bi-youtube"></i>
                        </a>
                    {% endif %}
                </div>
            </div>

            <!-- Col 2: Quick links -->
            <div>
                <h3 class="text-white font-semibold mb-4 text-sm uppercase tracking-wider">Quick Links</h3>
                <ul class="space-y-2 text-sm">
                    {% for link in footer_links %}
                        <li>
                            <a href="{{ link.url }}"
                               class="hover:text-white transition-colors">{{ link.label }}</a>
                        </li>
                    {% endfor %}
                </ul>
            </div>

            <!-- Col 3: extra block for pages to fill -->
            <div>{% block footer_extra %}{% endblock %}</div>
        </div>

        <div class="border-t border-gray-800 py-6 text-center text-xs text-gray-500">
            {{ site.footer_text }}
        </div>
    </footer>

    <!-- Toast notification (Alpine.js) -->
    <div x-data="{ show: false, message: '', type: 'success' }"
         x-on:toast.window="show = true; message = $event.detail.message; type = $event.detail.type || 'success'; setTimeout(() => show = false, 3500)"
         x-show="show"
         x-transition
         class="fixed top-20 left-1/2 -translate-x-1/2 z-[9999] px-5 py-2.5 rounded-lg text-white text-sm font-medium shadow-lg"
         :class="type === 'error' ? 'bg-red-600' : 'bg-gray-900'">
        <span x-text="message"></span>
    </div>

    {% block scripts %}{% endblock %}

</body>
</html>
```

- [ ] **Step 2: Add `GOOGLE_ANALYTICS` to context**

In `project/settings/base.py`, add at the bottom:
```python
GOOGLE_ANALYTICS = ''
```

In `project/settings/development.py`, override:
```python
GOOGLE_ANALYTICS = env('GOOGLE_ANALYTICS', default='')
```

In `project/settings/production.py`, override:
```python
GOOGLE_ANALYTICS = env('GOOGLE_ANALYTICS', default='')
```

Add it to `core/context_processors.py`:
```python
from django.conf import settings

def site_config(request):
    # ... existing code ...
    return {
        'site': site,
        'nav_links': NavLink.objects.filter(is_active=True),
        'footer_links': FooterLink.objects.filter(is_active=True),
        'GOOGLE_ANALYTICS': getattr(settings, 'GOOGLE_ANALYTICS', ''),
    }
```

- [ ] **Step 3: Add `output.css` static path**

The compiled CSS lives at `templates/css/output.css`. Since `STATICFILES_DIRS` includes `templates/`, the static tag `{% static 'css/output.css' %}` will resolve correctly. Verify:

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py collectstatic --noinput 2>&1 | grep output.css
```
Expected: `Copying ... output.css`

- [ ] **Step 4: Verify page loads with no template errors**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py runserver
```
Open `http://127.0.0.1:8000/` — should render a navbar and footer with placeholder content. No 500 errors.

- [ ] **Step 5: Commit**

```bash
git add templates/html/base.html project/settings/ core/context_processors.py
git commit -m "feat: rewrite base.html with Alpine.js nav, Tailwind v4 classes, SiteConfig-driven footer"
```

---

## Task 11: Homepage section partials + home.html

**Files:**
- Modify: `templates/html/home.html`
- Create: all `templates/html/components/sections/*.html` files

- [ ] **Step 1: Write `templates/html/home.html`**

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Home{% endblock %}
{% block description %}{{ site.tagline }}{% endblock %}

{% block content %}
{% for section in homepage_sections %}

    {% if section.section_type == 'hero' %}
        {% include "components/sections/hero.html" %}

    {% elif section.section_type == 'about' %}
        {% include "components/sections/about.html" %}

    {% elif section.section_type == 'services' %}
        {% include "components/sections/services.html" %}

    {% elif section.section_type == 'team' %}
        {% include "components/sections/team.html" %}

    {% elif section.section_type == 'events' %}
        {% include "components/sections/upcoming-events.html" %}

    {% elif section.section_type == 'gallery' %}
        {% include "components/sections/gallery-preview.html" %}

    {% elif section.section_type == 'testimonials' %}
        {% include "components/sections/testimonials.html" %}

    {% elif section.section_type == 'partners' %}
        {% include "components/sections/partners.html" %}

    {% elif section.section_type == 'news' %}
        {% include "components/sections/latest-news.html" %}

    {% elif section.section_type == 'faq' %}
        {% include "components/sections/faq-preview.html" %}

    {% endif %}

{% endfor %}
{% endblock %}
```

- [ ] **Step 2: Create `templates/html/components/sections/hero.html`**

```html
{% load static %}
{% if hero %}
<section class="relative min-h-screen flex items-center justify-center overflow-hidden bg-gray-900 text-white">

    {% if hero.background_image %}
        <img src="{{ hero.background_image.url }}" alt=""
             class="absolute inset-0 w-full h-full object-cover opacity-40">
    {% endif %}

    <div class="relative z-10 max-w-4xl mx-auto px-6 text-center">
        <h1 class="text-4xl lg:text-6xl font-bold leading-tight mb-6">
            {{ hero.headline }}
        </h1>
        {% if hero.subheadline %}
        <p class="text-xl lg:text-2xl text-gray-300 mb-10 max-w-2xl mx-auto">
            {{ hero.subheadline }}
        </p>
        {% endif %}
        <a href="{{ hero.cta_url }}"
           class="inline-flex items-center gap-2 bg-primary hover:bg-primary/90 text-white font-semibold px-8 py-4 rounded-xl transition-colors duration-200 text-lg">
            {{ hero.cta_text }}
            <i class="bi bi-arrow-right"></i>
        </a>
    </div>
</section>
{% endif %}
```

- [ ] **Step 3: Create `templates/html/components/sections/about.html`**

```html
{% if about %}
<section class="section-padding bg-white">
    <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {% if about.image %}
            <div class="rounded-2xl overflow-hidden shadow-lg">
                <img src="{{ about.image.url }}" alt="{{ about.heading }}"
                     class="w-full h-full object-cover">
            </div>
            {% endif %}
            <div class="{{ about.image|yesno:',' }}lg:pl-4">
                <h2 class="section-title">{{ about.heading }}</h2>
                <div class="prose prose-lg text-gray-600 leading-relaxed">
                    {{ about.body|linebreaks }}
                </div>
                <a href="/about/" class="inline-flex items-center gap-2 mt-8 text-primary font-semibold hover:gap-3 transition-all">
                    Read more <i class="bi bi-arrow-right"></i>
                </a>
            </div>
        </div>
    </div>
</section>
{% endif %}
```

- [ ] **Step 4: Create `templates/html/components/sections/services.html`**

```html
{% if services %}
<section class="section-padding bg-surface">
    <div class="max-w-7xl mx-auto text-center">
        <h2 class="section-title">Our Services</h2>
        <p class="section-subtitle">What we offer</p>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-4">
            {% for service in services %}
            <div class="card p-8 text-center hover:shadow-md transition-shadow">
                <i class="bi {{ service.icon }} text-5xl text-primary mb-4 block"></i>
                <h3 class="text-xl font-semibold text-gray-900 mb-3">{{ service.title }}</h3>
                <p class="text-gray-600 leading-relaxed">{{ service.description }}</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endif %}
```

- [ ] **Step 5: Create `templates/html/components/sections/team.html`**

```html
{% if team_members %}
<section class="section-padding bg-white">
    <div class="max-w-7xl mx-auto text-center">
        <h2 class="section-title">Our Team</h2>
        <p class="section-subtitle">Meet the people behind the work</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 mt-4">
            {% for member in team_members %}
            <div class="flex flex-col items-center text-center">
                {% if member.photo %}
                    <img src="{{ member.photo.url }}" alt="{{ member.name }}"
                         class="w-28 h-28 rounded-full object-cover mb-4 shadow-md">
                {% else %}
                    <div class="w-28 h-28 rounded-full bg-gray-100 flex items-center justify-center mb-4">
                        <i class="bi bi-person text-5xl text-gray-400"></i>
                    </div>
                {% endif %}
                <h3 class="font-semibold text-gray-900 text-lg">{{ member.name }}</h3>
                <p class="text-primary text-sm mb-2">{{ member.role }}</p>
                {% if member.bio %}
                    <p class="text-gray-500 text-sm leading-relaxed">{{ member.bio }}</p>
                {% endif %}
                <div class="flex gap-3 mt-3 text-gray-400 text-lg">
                    {% if member.facebook %}<a href="{{ member.facebook }}" target="_blank" class="hover:text-primary"><i class="bi bi-facebook"></i></a>{% endif %}
                    {% if member.twitter %}<a href="{{ member.twitter }}" target="_blank" class="hover:text-primary"><i class="bi bi-twitter-x"></i></a>{% endif %}
                    {% if member.linkedin %}<a href="{{ member.linkedin }}" target="_blank" class="hover:text-primary"><i class="bi bi-linkedin"></i></a>{% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endif %}
```

- [ ] **Step 6: Create `templates/html/components/sections/testimonials.html`**

```html
{% if testimonials %}
<section class="section-padding bg-primary text-white"
         x-data="{ current: 0, total: {{ testimonials|length }} }"
         x-init="setInterval(() => current = (current + 1) % total, 5000)">
    <div class="max-w-3xl mx-auto text-center">
        <h2 class="text-3xl lg:text-4xl font-bold mb-12">What People Say</h2>
        <div class="relative overflow-hidden min-h-[200px]">
            {% for testimonial in testimonials %}
            <div x-show="current === {{ forloop.counter0 }}"
                 x-transition:enter="transition ease-out duration-500"
                 x-transition:enter-start="opacity-0 translate-x-4"
                 x-transition:enter-end="opacity-100 translate-x-0"
                 class="absolute inset-0 flex flex-col items-center gap-4 px-4">
                {% if testimonial.photo %}
                    <img src="{{ testimonial.photo.url }}" alt="{{ testimonial.name }}"
                         class="w-16 h-16 rounded-full object-cover border-2 border-white/30">
                {% endif %}
                <blockquote class="text-xl italic text-white/90 leading-relaxed">
                    "{{ testimonial.quote }}"
                </blockquote>
                <cite class="not-italic">
                    <span class="font-semibold">{{ testimonial.name }}</span>
                    {% if testimonial.role or testimonial.organization %}
                        <span class="text-white/70"> — {{ testimonial.role }}{% if testimonial.organization %}, {{ testimonial.organization }}{% endif %}</span>
                    {% endif %}
                </cite>
            </div>
            {% endfor %}
        </div>
        <!-- Dots -->
        <div class="flex justify-center gap-2 mt-16">
            {% for testimonial in testimonials %}
            <button @click="current = {{ forloop.counter0 }}"
                    class="w-2.5 h-2.5 rounded-full transition-colors"
                    :class="current === {{ forloop.counter0 }} ? 'bg-white' : 'bg-white/30'"
                    aria-label="Testimonial {{ forloop.counter }}">
            </button>
            {% endfor %}
        </div>
    </div>
</section>
{% endif %}
```

- [ ] **Step 7: Create `templates/html/components/sections/partners.html`**

```html
{% if partners %}
<section class="section-padding bg-white">
    <div class="max-w-7xl mx-auto text-center">
        <h2 class="section-title">Our Partners</h2>
        <div class="flex flex-wrap justify-center items-center gap-10 mt-8">
            {% for partner in partners %}
            {% if partner.website_url %}
            <a href="{{ partner.website_url }}" target="_blank" rel="noopener noreferrer"
               class="opacity-60 hover:opacity-100 transition-opacity">
                <img src="{{ partner.logo.url }}" alt="{{ partner.name }}" class="h-12 w-auto object-contain">
            </a>
            {% else %}
            <img src="{{ partner.logo.url }}" alt="{{ partner.name }}"
                 class="h-12 w-auto object-contain opacity-60">
            {% endif %}
            {% endfor %}
        </div>
    </div>
</section>
{% endif %}
```

- [ ] **Step 8: Create `templates/html/components/sections/latest-news.html`**

```html
{% if latest_blogs %}
<section class="section-padding bg-surface">
    <div class="max-w-7xl mx-auto">
        <div class="flex items-center justify-between mb-10">
            <h2 class="section-title mb-0">Latest News</h2>
            <a href="/blog/" class="text-primary font-semibold hover:underline text-sm flex items-center gap-1">
                All posts <i class="bi bi-arrow-right"></i>
            </a>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {% for blog in latest_blogs %}
            <a href="{% url 'get-blog' slug=blog.slug %}" class="card hover:shadow-md transition-shadow group">
                {% if blog.thumbnail %}
                <div class="aspect-video overflow-hidden">
                    <img src="{{ blog.thumbnail.url }}" alt="{{ blog.title }}"
                         class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                </div>
                {% endif %}
                <div class="p-6">
                    <h3 class="font-semibold text-gray-900 text-lg mb-2 group-hover:text-primary transition-colors">
                        {{ blog.title }}
                    </h3>
                    <p class="text-gray-500 text-sm">
                        {{ blog.datetime|date:"N j, Y" }}
                    </p>
                </div>
            </a>
            {% endfor %}
        </div>
    </div>
</section>
{% endif %}
```

- [ ] **Step 9: Create stub partials for Plan B sections**

These render nothing (Plan B fills them in):

`templates/html/components/sections/upcoming-events.html`:
```html
{# Stub — filled in Plan B (events app) #}
{% if upcoming_events %}
<section class="section-padding bg-white">
    <div class="max-w-7xl mx-auto text-center">
        <h2 class="section-title">Upcoming Events</h2>
    </div>
</section>
{% endif %}
```

`templates/html/components/sections/gallery-preview.html`:
```html
{# Stub — filled in Plan B (gallery app) #}
{% if gallery_images %}
<section class="section-padding bg-surface">
    <div class="max-w-7xl mx-auto text-center">
        <h2 class="section-title">Gallery</h2>
    </div>
</section>
{% endif %}
```

`templates/html/components/sections/faq-preview.html`:
```html
{# Stub — filled in Plan B (faq app) #}
{% if faq_items %}
<section class="section-padding bg-white">
    <div class="max-w-7xl mx-auto text-center">
        <h2 class="section-title">FAQ</h2>
    </div>
</section>
{% endif %}
```

- [ ] **Step 10: Add Tailwind compile step (watch mode for dev)**

In development, run this alongside `runserver`:
```bash
./bin/tailwindcss -i styling/static_src/input.css -o templates/css/output.css --watch
```

After adding new template files, recompile so new utility classes are included:
```bash
./bin/tailwindcss -i styling/static_src/input.css -o templates/css/output.css --minify
```

- [ ] **Step 11: Verify homepage renders**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py runserver
```
Open `http://127.0.0.1:8000/`. Verify: navbar, hero, at least one section (depending on which have data), footer. No 500 errors, no broken layout.

- [ ] **Step 12: Run all tests**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests -v 2
```
Expected: all tests pass.

- [ ] **Step 13: Commit**

```bash
git add templates/
git commit -m "feat: homepage section partials and home.html assembly"
```

---

## Task 12: Standalone pages + final wiring

**Files:**
- Modify: `templates/html/about.html`
- Modify: `templates/html/services.html`
- Modify: `templates/html/blog/blog-list.html` (update CSS classes to Tailwind v4, no prefix)
- Modify: `templates/html/blog/blog-view.html`
- Modify: `templates/html/inquiry/inquiry-create.html`

- [ ] **Step 1: Write `templates/html/about.html`**

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}About Us{% endblock %}
{% block description %}Learn more about {{ site.site_name }}{% endblock %}

{% block content %}

<!-- About section -->
{% if about %}
<section class="section-padding bg-white">
    <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {% if about.image %}
            <div class="rounded-2xl overflow-hidden shadow-lg order-2 lg:order-1">
                <img src="{{ about.image.url }}" alt="{{ about.heading }}" class="w-full h-full object-cover">
            </div>
            {% endif %}
            <div class="order-1 lg:order-2">
                <h1 class="section-title">{{ about.heading }}</h1>
                <div class="prose prose-lg text-gray-600 leading-relaxed">
                    {{ about.body|linebreaks }}
                </div>
            </div>
        </div>
    </div>
</section>
{% endif %}

<!-- Team section -->
{% if team_members %}
<section class="section-padding bg-surface">
    <div class="max-w-7xl mx-auto text-center">
        <h2 class="section-title">Our Team</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 mt-4">
            {% for member in team_members %}
            <div class="flex flex-col items-center text-center">
                {% if member.photo %}
                    <img src="{{ member.photo.url }}" alt="{{ member.name }}"
                         class="w-28 h-28 rounded-full object-cover mb-4 shadow-md">
                {% else %}
                    <div class="w-28 h-28 rounded-full bg-gray-100 flex items-center justify-center mb-4">
                        <i class="bi bi-person text-5xl text-gray-400"></i>
                    </div>
                {% endif %}
                <h3 class="font-semibold text-gray-900 text-lg">{{ member.name }}</h3>
                <p class="text-primary text-sm mb-2">{{ member.role }}</p>
                {% if member.bio %}
                    <p class="text-gray-500 text-sm leading-relaxed">{{ member.bio }}</p>
                {% endif %}
                <div class="flex gap-3 mt-3 text-gray-400 text-lg">
                    {% if member.facebook %}<a href="{{ member.facebook }}" target="_blank" class="hover:text-primary"><i class="bi bi-facebook"></i></a>{% endif %}
                    {% if member.twitter %}<a href="{{ member.twitter }}" target="_blank" class="hover:text-primary"><i class="bi bi-twitter-x"></i></a>{% endif %}
                    {% if member.linkedin %}<a href="{{ member.linkedin }}" target="_blank" class="hover:text-primary"><i class="bi bi-linkedin"></i></a>{% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endif %}

{% endblock %}
```

- [ ] **Step 2: Write `templates/html/services.html`**

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Services{% endblock %}
{% block description %}Services and programmes offered by {{ site.site_name }}{% endblock %}

{% block content %}
<section class="section-padding">
    <div class="max-w-7xl mx-auto">
        <h1 class="section-title text-center">Our Services</h1>
        <p class="section-subtitle text-center">What we offer</p>
        {% if services %}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {% for service in services %}
            <div class="card p-8 text-center hover:shadow-md transition-shadow">
                <i class="bi {{ service.icon }} text-5xl text-primary mb-4 block"></i>
                <h2 class="text-xl font-semibold text-gray-900 mb-3">{{ service.title }}</h2>
                <p class="text-gray-600 leading-relaxed">{{ service.description }}</p>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <p class="text-center text-gray-500 mt-10">No services listed yet.</p>
        {% endif %}
    </div>
</section>
{% endblock %}
```

- [ ] **Step 3: Update `templates/html/blog/blog-list.html`**

Replace all `tw-` prefixed classes with unprefixed Tailwind v4 equivalents. Key replacements:
- `tw-flex` → `flex`
- `tw-mt-[5%]` → `mt-[5%]`
- `tw-text-3xl` → `text-3xl`
- `tw-w-full` → `w-full`
- `tw-min-h-[100vh]` → `min-h-screen`
- `tw-p-3` → `p-3`
- `md:tw-px-[15%]` → `md:px-[15%]`

Also update the base template extend path:
```html
{% extends 'base.html' %}
```

- [ ] **Step 4: Update `templates/html/blog/blog-view.html`**

Apply the same `tw-` prefix removal. Also update extend to `{% extends 'base.html' %}`.

- [ ] **Step 5: Update `templates/html/inquiry/inquiry-create.html`**

Apply `tw-` prefix removal. Update extend to `{% extends 'base.html' %}`. Update form action URL name if needed (still `contact-us`).

- [ ] **Step 6: Compile Tailwind with all new templates**

```bash
./bin/tailwindcss -i styling/static_src/input.css -o templates/css/output.css --minify
```

- [ ] **Step 7: Run all tests**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests -v 2
```
Expected: all tests pass.

- [ ] **Step 8: Smoke test all pages**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py runserver
```

Visit and verify each page loads without errors:
- `http://127.0.0.1:8000/` — homepage
- `http://127.0.0.1:8000/about/` — about + team
- `http://127.0.0.1:8000/services/` — services
- `http://127.0.0.1:8000/blog/` — blog list
- `http://127.0.0.1:8000/contact/` — contact form
- `http://127.0.0.1:8000/admin/` — admin panel

- [ ] **Step 9: Commit**

```bash
git add templates/
git commit -m "feat: standalone pages, update blog/inquiry templates to Tailwind v4"
```

---

## Task 13: Final compilation and README update

- [ ] **Step 1: Final Tailwind compile**

```bash
./bin/tailwindcss -i styling/static_src/input.css -o templates/css/output.css --minify
```

- [ ] **Step 2: Run collectstatic to verify no broken references**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py collectstatic --noinput 2>&1 | tail -5
```
Expected: no errors, static files copied.

- [ ] **Step 3: Run full test suite**

```bash
DJANGO_SETTINGS_MODULE=project.settings.development python manage.py test tests -v 2
```
Expected: all tests pass.

- [ ] **Step 4: Update `.gitignore`**

Ensure this is in `.gitignore`:
```
# Python
*.pyc
__pycache__/
*.pyo

# Django
db.sqlite3
media/
staticfiles/
.env
.env.local

# Tailwind binary
bin/tailwindcss
bin/tailwindcss.exe

# IDE
.vscode/
.idea/
```

- [ ] **Step 5: Final commit**

```bash
git add .
git commit -m "chore: Plan A complete — Django 5.2, Tailwind v4, core app, cPanel deployment"
```

---

## Self-Review Checklist (completed before publishing)

- [x] **Spec coverage:** Django 5.2 ✓, Tailwind v4 ✓, Alpine.js ✓, settings split ✓, Firebase removal ✓, SiteConfig ✓, HomepageSection ordering ✓, HeroSection/AboutSection/TeamMember/Service/Testimonial/Partner ✓, NavLink/FooterLink ✓, data migration defaults ✓, context processor ✓, passenger_wsgi.py ✓, .env.example ✓, base.html rewrite ✓, section partials ✓, about/services pages ✓, blog/inquiry template update ✓
- [x] **No placeholders:** All steps have complete code
- [x] **Type consistency:** Model names match across tasks (SiteConfig pk=1 enforced in save, HomepageSection.section_type choices consistent in model and home.html)
- [x] **Plan B gap:** events/gallery/faq apps are stubs — explicitly noted as Plan B scope

---

## What Plan B Covers

After this plan ships:
- `events` app: Event model, list/detail views, `/events/` and `/events/<slug>/` pages, fill in `upcoming-events.html` partial
- `gallery` app: GalleryCategory + GalleryImage, Alpine.js filter grid, fill in `gallery-preview.html` partial
- `faq` app: FAQItem, Alpine.js accordion, `/faq/` page, fill in `faq-preview.html` partial
- Newsletter form backend
- 404/rate-limit error page styling
- SEO: sitemap entries for events, gallery
