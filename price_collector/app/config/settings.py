import os


class Config:
    COLLECTOR_SERVER_NAME = os.getenv('COLLECTOR_SERVER_NAME', '')
    SESSION_COOKIE_DOMAIN = os.getenv('SESSION_COOKIE_DOMAIN', '')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', '')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', '')

CurrentConfig = Config()

