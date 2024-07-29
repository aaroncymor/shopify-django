import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
APP_NAME = os.getenv("APP_NAME", "project_name")
APP_ENV = os.getenv("APP_ENV", "dev")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{APP_NAME}.settings")

app = Celery(f"{APP_NAME}")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "delete_job_files": {
        # Every 1 minute for testing purposes
        "schedule": crontab(minute="*/1"),
    },
}

app.conf.timezone = "UTC"
