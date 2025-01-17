import os
import logging
from flask import Flask
from yp_fin_utils.db.connection import setup_mongodb_connection
from yp_fin_utils.utils.logging import configure_logging
from app.routes import register_routes


logger = logging.getLogger(__name__)

def run_app():
    app = create_app()
    return app

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

    setup_mongodb_connection()

    configure_logging('data/logs/app.log')

    register_routes(app)

    return app
