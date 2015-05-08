from __future__ import absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')

from django.conf import settings
# set the celery project object as app
app = Celery('tutorial')

# Using a string here means the worker will not have to pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler",
    BROKER_URL = 'django://',
)
