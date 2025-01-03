from .api_routes import register_api_routes
from .job_routes import register_job_routes

def register_routes(app):
    # RESTful API 라우팅 등록
    register_api_routes(app)
    
    # 작업 스케줄링 등록 (필요시)
    register_job_routes(app)

