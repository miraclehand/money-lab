import logging
from flask import Flask
from flask_cors import CORS
from yp_fin_utils.db.connection import setup_mongodb_connection
from yp_fin_utils.utils.logging import configure_logging
from app.config.settings import CurrentConfig
from app.routes import register_routes


logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    configure_server(app)

    setup_mongodb_connection()

    configure_logging('data/logs/app.log')

    CORS(app)

    register_routes(app)
    return app

def configure_server(app):
    app.config['SERVER_NAME'] = CurrentConfig.SERVER_NAME
    app.config['SESSION_COOKIE_DOMAIN'] = CurrentConfig.SESSION_COOKIE_DOMAIN
