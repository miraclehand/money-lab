import os
import logging
import datetime
from flask import Flask
from flask_cors import CORS
from pymodm import connect
from apscheduler.schedulers.background import BackgroundScheduler
from yp_fin_utils.utils.logging import configure_logging
from app.routes import register_routes
from app.celery_worker.tasks.stock_task import put_stock_data
from app.celery_worker.tasks.candle_task import put_candle_data


logger = logging.getLogger(__name__)
def run_app():
    app = create_app()

    scheduler = initialize_scheduler()
    try:
        # 한번만 실행하기 위해서 아래 코드 필요함.
        if os.environ.get("WERKZEUG_RUN_MAIN") == 'true':
            scheduler.start()
            logger.info('scheduler.start()')
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
    except Exception as e:
        scheduler.shutdown()
        raise RuntimeError(f"Application startup failed: {str(e)}")
    return app

def create_app():
    app = Flask(__name__)

    configure_server(app)
    setup_mongodb_connection()
    configure_logging('data/logs/app.log')

    CORS(app)

    register_routes(app)
    return app

def configure_server(app):
    app.config['SERVER_NAME'] = os.getenv('COLLECTOR_SERVER_NAME')
    app.config['SESSION_COOKIE_DOMAIN'] = os.getenv('SESSION_COOKIE_DOMAIN')
    app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
    app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND')

def setup_mongodb_connection():
    mongo_uri = os.getenv("MONGO_URI", "localhost")
    connection_alias = os.getenv("CONNECTION_ALIAS", "")
    connect(mongo_uri, alias=connection_alias, connect=False)

def initialize_scheduler():
    scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Seoul'})

    scheduler.add_job(put_candle_data, 'cron', day_of_week='mon-fri', hour=16, minute=30, args=['kr'])
    scheduler.add_job(put_stock_data,  'cron', day_of_week='mon-fri', hour=21, minute=0, args=['kr'])

    return scheduler
