import os


class Config:
    DART_API_KEY = os.getenv('DART_API_KEY', '')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', '')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', '')

CurrentConfig = Config()

