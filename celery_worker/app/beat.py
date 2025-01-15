import os
from celery import Celery
from celery.schedules import crontab


def create_celery(app_name=__name__):
    broker = os.getenv('CELERY_BROKER_URL', '')
    backend = os.getenv('CELERY_RESULT_BACKEND', '')

    celery = Celery(app_name, broker=broker, backend=backend)

    celery.conf.result_backend = backend
    celery.conf.update(
        result_expires=3600,
        timezone='Asia/Seoul',
        enable_utc=False
    )
    celery.conf.beat_schedule = {
        'put-stock-data-at-4:30pm': {
            'task': 'app.tasks.stock_task.put_candle_data',
            'schedule': crontab(hour=4, minute=30),
            'args': ['kr'],
        },
    }
    return celery

celery = create_celery()
