import os
from celery import Celery

# Sets default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pnb_main.settings') 

# Creates the Celery app
app = Celery('pnb_main')

# Loads custom config from Django settings, using CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discovers tasks from all apps in your Django project
app.autodiscover_tasks()