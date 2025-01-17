from app.routes.job_routes import job_routes


def register_routes(app):
    app.register_blueprint(job_routes)

