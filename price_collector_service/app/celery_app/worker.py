import os
import glob
from celery import Celery
from yp_fin_utils.utils.logging import configure_logging
from yp_fin_utils.db.connection import setup_mongodb_connection


def create_celery(app_name=__name__):
    broker = os.getenv('CELERY_BROKER_URL', '')
    backend = os.getenv('CELERY_RESULT_BACKEND', '')

    celery = Celery(app_name, broker=broker, backend=backend)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tasks'))
    module_base = base_dir.replace('/app/', '').replace(os.sep, '.')

    task_modules = [
        f'{module_base}.{os.path.relpath(path, base_dir).replace(os.sep, ".").rsplit(".", 1)[0]}'
        for path in glob.glob(os.path.join(base_dir, '**', '*.py'), recursive=True)
        if not path.endswith('__init__.py')
    ]
    celery.autodiscover_tasks(task_modules)

    celery.conf.update(
        task_default_queue='price_queue',
        result_backend=backend,
        broker_connection_retry_on_startup = True,
    )
    return celery

celery = create_celery()
setup_mongodb_connection()
