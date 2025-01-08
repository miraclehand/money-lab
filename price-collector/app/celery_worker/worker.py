import os
from pymodm import connect
from app.celery_worker.celery_config import make_celery
from app.utils.logging import configure_logging


def create_celery():
    broker = os.getenv("CELERY_BROKER_URL", "")
    backend = os.getenv("CELERY_RESULT_BACKEND", "")
    celery = make_celery(__name__, broker, backend)
    return celery


def setup_mongodb_connection():
    mongo_uri = os.getenv("MONGO_URI", "localhost")
    connection_alias = os.getenv("CONNECTION_ALIAS", "")
    connect(mongo_uri, alias=connection_alias, connect=False)

setup_mongodb_connection()
configure_logging()
celery = create_celery()
