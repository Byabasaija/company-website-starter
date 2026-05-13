# Company Website Starter

A production-ready Django CMS template for agencies and freelancers. Generate a fully-featured company website in minutes with a single command.

![Company Website Starter](django-website-template.png)

## What you get

A complete content-managed website with an admin panel where clients control everything — no code changes needed for day-to-day content.

| Feature | Details |
|---|---|
| **Hero** | Slideshow or static background, configurable slides |
| **Services** | Card grid, list, or showcase layout (swappable variants) |
| **About** | Default or centered variant |
| **Partners** | Auto-marquee (5+ logos) or static grid |
| **Team / Profiles** | Category-based people pages (`/profiles/<category>/<person>/`) |
| **Events** | Upcoming/past split, countdown timer, organizer & sponsor fields |
| **Blog** | Trix rich-text editor, categories, SEO fields |
| **Gallery** | Image collections with category filter |
| **FAQ** | Alpine.js accordion |
| **Newsletter** | Subscription with unsubscribe |
| **Contact** | Split-panel form with reCAPTCHA support, country dial-code picker |
| **Composable pages** | Admin-assembled pages with drag-and-drop section ordering |
| **Section variants** | Drop a new `variant.html` into any section folder — no code changes |
| **Navigation** | Admin-managed nav & footer links, nested dropdowns, auto-URL from page FK |
| **Branding** | Primary/secondary colour, logo, favicon, tagline all via admin |
| **SEO** | Sitemap.xml, robots.txt, Open Graph, Google Analytics |
| **Deployment-ready** | Vercel, Railway, Render — Procfile + `vercel.json` included |

**Stack:** Django 5.2 LTS · Tailwind CSS v4 (standalone CLI) · Alpine.js 3 · Bootstrap Icons

---

## Quickstart (cookiecutter)

```bash
pip install cookiecutter
cookiecutter gh:your-org/company-website-starter
```

You will be prompted for:

| Prompt | Example |
|---|---|
| `project_name` | `UCF Chess Club` |
| `project_slug` | `ucf_chess` (auto-generated) |
| `site_name` | `UCF Chess Club` |
| `primary_color` | `#1a56a0` |
| `author_email` | `admin@ucfchess.org` |

The post-generation hook installs dependencies, runs migrations, loads the initial `SiteConfig`, compiles Tailwind, and creates a `.env` file automatically.

```bash
cd ucf_chess
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/` to start configuring your site.

---

## Manual setup

1. Clone the repo and enter the generated project directory.

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file (or `.env.local` for development):
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```
   Generate a secret key:
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

4. Run migrations and load initial data:
   ```bash
   python manage.py migrate
   python manage.py loaddata fixtures/initial.json
   ```

5. Download and compile Tailwind (if not done by the hook):
   ```bash
   # macOS arm64
   curl -sL https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64 -o bin/tailwindcss
   chmod +x bin/tailwindcss
   bin/tailwindcss -i styling/static_src/input.css -o templates/css/output.css --minify
   ```

6. Create a superuser and run the server:
   ```bash
   python manage.py createsuperuser
   python manage.py runserver
   ```

---

## Customisation

### Change branding
Go to **Admin → Site Configuration**. Update site name, tagline, logo, favicon, colours, social links, and contact details. No code changes required.

### Homepage sections
Go to **Admin → Homepage Sections**. Enable, reorder, and change the variant of any section by choosing from the available `variant` options.

Available variants per section type:

| Section | Variants |
|---|---|
| `services` | `default` (card grid), `list`, `showcase` |
| `about` | `default`, `centered` |
| `team` | `default`, `minimal` |
| `testimonials` | `default`, `grid` |

### Add a new section variant
Create a file at `templates/html/components/sections/<type>/<variant>.html`. It is automatically available in the admin variant dropdown — no code changes needed.

### Tailwind development (watch mode)
```bash
bin/tailwindcss -i styling/static_src/input.css -o templates/css/output.css --watch
```

### Template tags
```django
{% block title %}Page Title{% endblock %}
{% block description %}Meta description{% endblock %}
{% block socialTitle %}OG title{% endblock %}
{% block socialDescription %}OG description{% endblock %}
{% block pageImage %}{% endblock %}     {# OG image URL #}
{% block head_tags %}{% endblock %}     {# extra <head> tags #}
{% block scripts %}{% endblock %}       {# scripts before </body> #}
```

---

## Project structure

```
<project_slug>/
├── <project_slug>/         # Django project package (settings, urls, wsgi)
│   └── settings/
│       ├── base.py
│       ├── development.py
│       └── production.py
├── core/                   # SiteConfig, HomepageSection, NavLink, Hero, Services, etc.
├── blog/                   # Blog with Trix editor
├── events/                 # Events with countdown
├── gallery/                # Image gallery
├── faq/                    # FAQ accordion
├── profiles/               # People / team profiles with categories
├── newsletter/             # Email newsletter subscription
├── inquiry/                # Contact form with reCAPTCHA
├── pages/                  # Composable CMS pages
├── user/                   # Custom user model
├── utils/                  # Shared helpers
├── templates/              # All HTML, CSS, JS, and static assets
│   ├── html/
│   │   ├── base.html
│   │   ├── components/sections/  # Section partials with variant subdirs
│   │   └── ...
│   └── css/output.css
├── styling/static_src/     # Tailwind input source
├── fixtures/initial.json   # Seed data (SiteConfig)
└── tests/
```

---

## Deployment

### Vercel
```bash
python manage.py collectstatic
```
Set environment variables in the Vercel dashboard, then push. The `vercel.json` is pre-configured.

### Railway / Render
Use the included `Procfile`:
```
web: gunicorn <project_slug>.wsgi --log-file -
```
Set `DEBUG=False`, `SECRET_KEY`, `ALLOWED_HOSTS`, and your database URL.

### Key production environment variables
```
SECRET_KEY=
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgres://...
GOOGLE_ANALYTICS=G-XXXXXXXXXX
RECAPTCHA_SITE_KEY=
RECAPTCHA_SECRET_KEY=
```

---

## Running tests

```bash
python manage.py test tests/
```

---

## License

MIT — free to use for personal and commercial projects. Attribution appreciated but not required.
