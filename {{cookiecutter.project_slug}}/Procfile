release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn project.wsgi:application --workers 2 --bind 0.0.0.0:$PORT