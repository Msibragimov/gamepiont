from celery import Celery
from django.conf import settings
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyberbase.settings')
app = Celery('testsite')



app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)