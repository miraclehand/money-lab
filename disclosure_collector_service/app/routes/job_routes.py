from flask import Blueprint, request
from celery import Celery
from app.config.settings import CurrentConfig


job_routes = Blueprint('job_routes', __name__)
celery = Celery('disclosure_collector', broker=CurrentConfig.CELERY_BROKER_URL, backend=CurrentConfig.CELERY_RESULT_BACKEND)

@job_routes.route('/jobs/disclosure/<string:country>', methods=['POST', 'PUT', 'DELETE'])
@job_routes.route('/jobs/disclosure/<string:country>/<string:start_date>/<string:end_date>', methods=['POST', 'PUT', 'DELETE'])
def manage_disclosure_data_route(country, start_date=None, end_date=None):
    disclosure_type = 'DIVIDEND'
    queue = 'disclosure_queue'

    if request.method == 'POST':
        result = celery.send_task('app.tasks.data_sync.disclosure_task.refresh_disclosure_data', args=[country, disclosure_type, start_date, end_date], queue=queue)
    elif request.method == 'PUT':
        result = celery.send_task('app.tasks.data_sync.disclosure_task.sync_disclosure_data', args=[country, disclosure_type, start_date, end_date], queue=queue)
    elif request.method == 'DELETE':
        result = celery.send_task('app.tasks.data_sync.disclosure_task.delete_disclosure_data', args=[country, disclosure_type, start_date, end_date], queue=queue)
    return {'message': f'{country}의 공시 데이터 갱신 요청이 시작되었습니다.'}, 202
