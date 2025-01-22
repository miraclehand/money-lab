from flask import Blueprint, request
from celery import Celery
from app.config.settings import CurrentConfig


job_routes = Blueprint('job_routes', __name__)
celery = Celery('price_collector', broker=CurrentConfig.CELERY_BROKER_URL, backend=CurrentConfig.CELERY_RESULT_BACKEND)

@job_routes.route('/jobs/stocks/<string:country>', methods=['POST', 'PUT', 'DELETE'])
@job_routes.route('/jobs/stocks/<string:country>/<string:ticker>', methods=['POST', 'PUT', 'DELETE'])
def manage_stock_data_route(country, ticker=None):
    queue = 'price_queue'

    if request.method == 'POST':
        result = celery.send_task('app.tasks.data_sync.stock_task.refresh_stock_data', args=[country, ticker], queue=queue)
    elif request.method == 'PUT':
        result = celery.send_task('app.tasks.data_sync.stock_task.sync_stock_data', args=[country, ticker], queue=queue)
    elif request.method == 'DELETE':
        result = celery.send_task('app.tasks.data_sync.stock_task.delete_stock_data', args=[country, ticker], queue=queue)
    return {'message': f'{country}의 {ticker or "전체"} 주식 데이터 갱신 요청이 시작되었습니다.'}, 202

@job_routes.route('/jobs/candles/<string:country>', methods=['POST', 'PUT', 'DELETE'])
@job_routes.route('/jobs/candles/<string:country>/<string:ticker>', methods=['POST', 'PUT', 'DELETE'])
def manage_candle_data_route(country, ticker=None):
    queue = 'price_queue'

    if request.method == 'POST':
        result = celery.send_task('app.tasks.data_sync.candle_task.refresh_candle_data', args=[country, ticker], queue=queue)
    elif request.method == 'PUT':
        result = celery.send_task('app.tasks.data_sync.candle_task.sync_candle_data', args=[country, ticker], queue=queue)
    elif request.method == 'DELETE':
        result = celery.send_task('app.tasks.data_sync.candle_task.delete_candle_data', args=[country, ticker], queue=queue)
    return {'message': f'{country}의 {ticker or "전체"} 주가 데이터 갱신 요청이 시작되었습니다.'}, 202
