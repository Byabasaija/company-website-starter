# {{cookiecutter.project_name}}

A production-ready company website built with Django, Tailwind CSS v4, and Alpine.js.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Environment variables

Copy `.env.example` to `.env.local` (development) or `.env` (production) and fill in:

```
SECRET_KEY=
DATABASE_URL=postgres://...
```

## Tailwind

```bash
bin/tailwindcss -i styling/static_src/input.css -o templates/css/output.css --watch
```

## Deployment

Set `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, and `DATABASE_URL` on your host, then:

```bash
python manage.py collectstatic
```

---

Generated with [company-website-starter](https://github.com/Byabasaija/company-website-starter)
