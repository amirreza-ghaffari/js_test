import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'js_test.settings')
app = Celery('bcm')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Asia/Tehran'
app.conf.use_tz = True
app.autodiscover_tasks()

