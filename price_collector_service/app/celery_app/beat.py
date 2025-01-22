import os
from celery import Celery
from celery.schedules import crontab


def create_celery(app_name=__name__):
    broker = os.getenv('CELERY_BROKER_URL', '')
    backend = os.getenv('CELERY_RESULT_BACKEND', '')

    celery = Celery(app_name, broker=broker, backend=backend)

    celery.conf.update(
        result_backend=backend,
        result_expires=3600,
        timezone='Asia/Seoul',
        enable_utc=False,
        broker_connection_retry_on_startup = True,
        beat_schedule = {
            'put-candle-data-at-4:30pm': {
                'task': 'app.tasks.data_sync.candle_task.sync_candle_data',
                'schedule': crontab(hour=16, minute=30),
                'args': ['kr'],
                'options': {
                    'queue': 'price_queue'
                }
            },
        },
    )
    return celery

celery = create_celery()
