import os
import glob
from celery import Celery


def create_celery(app_name=__name__):
    broker = os.getenv('CELERY_BROKER_URL', '')
    backend = os.getenv('CELERY_RESULT_BACKEND', '')

    celery = Celery(app_name, broker=broker, backend=backend)
    task_modules = glob.glob(os.path.join(os.path.dirname(__file__), 'tasks', '*.py'))
    task_modules = [
        f'app.tasks.{os.path.splitext(os.path.basename(path))[0].replace("/app", "")}'
        for path in task_modules if not path.endswith('__init__.py')
    ]

    celery.autodiscover_tasks(task_modules)
    celery.conf.result_backend = backend
    return celery
