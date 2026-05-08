import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.production')

from project.wsgi import application
