import os
from yp_fin_utils.db.connection import setup_mongodb_connection
from yp_fin_utils.utils.logging import configure_logging
from app.celery_worker.celery_config import make_celery


def create_celery():
    broker = os.getenv("CELERY_BROKER_URL", "")
    backend = os.getenv("CELERY_RESULT_BACKEND", "")
    celery = make_celery(__name__, broker, backend)
    return celery

setup_mongodb_connection()

configure_logging('data/logs/app.log')
celery = create_celery()
