import os
from flask import Flask
from flask_cors import CORS
from pymodm import connect
from app.routes import register_routes


def create_app():
    app = Flask(__name__)

    _configure_server(app)
    _setup_mongodb_connection()
    register_routes(app)
    CORS(app)

    return app

def _configure_server(app):
    app.config['SERVER_NAME'] = os.getenv('COLLECTOR_SERVER_NAME')
    app.config['SESSION_COOKIE_DOMAIN'] = os.getenv('SESSION_COOKIE_DOMAIN')

def _setup_mongodb_connection():
    mongo_uri = os.getenv("MONGO_URI", "localhost")
    connection_alias = os.getenv("CONNECTION_ALIAS", "")
    connect(mongo_uri, alias=connection_alias, connect=False)
