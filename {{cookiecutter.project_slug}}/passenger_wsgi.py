import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__PROJECT_SLUG__.settings.production')

from __PROJECT_SLUG__.wsgi import application
