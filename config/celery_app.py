import os 
from django.conf import settings 
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.local")

app = Celery("alpha_apartments")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)