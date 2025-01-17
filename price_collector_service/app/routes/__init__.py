from app.routes.api_routes import api_routes
from app.routes.job_routes import job_routes


def register_routes(app):
    app.register_blueprint(api_routes)
    app.register_blueprint(job_routes)

