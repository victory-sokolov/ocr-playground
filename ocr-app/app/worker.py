import os

from celery import Celery

app = Celery("ocrapp")


app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6389")
app.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6389",
)
