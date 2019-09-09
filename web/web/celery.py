from __future__ import absolute_import
import os, time
from celery import Celery, platforms

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
platforms.C_FORCE_ROOT = True

from django.conf import settings  # noqa

app = Celery('web')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task()
def judge_loop():
    import django
    django.setup()
    from interview.judge import judge
    while True:
        try:
            judge()
        except Exception as e:
            print(e)
        time.sleep(0.1)

judge_loop.delay()
