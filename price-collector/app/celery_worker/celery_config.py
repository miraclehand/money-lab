from celery import Celery


def make_celery(celery_name, broker, backend):
    celery = Celery(
        celery_name,
        broker=broker,
        backend=backend
    )

    celery.conf.update(
        task_routes={
            'app.tasks.*': {'queue': 'default'},
        }
    )
    return celery
