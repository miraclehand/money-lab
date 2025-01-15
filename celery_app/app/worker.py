from yp_fin_utils.db.connection import setup_mongodb_connection
from yp_fin_utils.utils.logging import configure_logging
from app.celery_config import create_celery

celery = create_celery()

setup_mongodb_connection()
configure_logging('data/logs/app.log')

"""
import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from yp_fin_utils.db.connection import setup_mongodb_connection
from yp_fin_utils.utils.logging import configure_logging
from app.tasks.candle_task import put_candle_data
from app.tasks.stock_task import put_stock_data


logger = logging.getLogger(__name__)

def initialize_and_start_scheduler():
    scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Seoul'})

    scheduler.add_job(put_candle_data, 'cron', day_of_week='mon-fri', hour=16, minute=30, args=['kr'])
    scheduler.add_job(put_stock_data,  'cron', day_of_week='mon-fri', hour=21, minute=0, args=['kr'])

    if os.environ.get("WERKZEUG_RUN_MAIN") == 'true':
        try:
            scheduler.start()
            logger.info('Scheduler started successfully')
        except Exception as e:
            logger.error(f"Failed to start scheduler: {str(e)}")
            scheduler.shutdown()
            raise RuntimeError(f"Scheduler startup failed: {str(e)}")
    else:
        logger.info("Skipping scheduler start - not running in main process")

    return scheduler
print('aaaaaaaaaaaaaaaaaaaaaaa')
print('aaaaaaaaaaaaaaaaaaaaaaa')
print('aaaaaaaaaaaaaaaaaaaaaaa')
print('aaaaaaaaaaaaaaaaaaaaaaa')
print('aaaaaaaaaaaaaaaaaaaaaaa')
print('aaaaaaaaaaaaaaaaaaaaaaa')
print('aaaaaaaaaaaaaaaaaaaaaaa')
print('aaaaaaaaaaaaaaaaaaaaaaa')

initialize_and_start_scheduler()
setup_mongodb_connection()
configure_logging('data/logs/app.log')
"""
