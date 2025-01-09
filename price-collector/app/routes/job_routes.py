from flask import Blueprint, request
from app.celery_worker.tasks.stock_task import post_stock_data, put_stock_data, delete_stock_data
from app.celery_worker.tasks.candle_task import post_candle_data, put_candle_data, delete_candle_data


job_routes = Blueprint('job_routes', __name__)

@job_routes.route('/jobs/stocks/<string:country>', methods=['POST', 'PUT', 'DELETE'])
@job_routes.route('/jobs/stocks/<string:country>/<string:ticker>', methods=['POST', 'PUT', 'DELETE'])
def manage_stock_data_route(country, ticker=None):
    if request.method == 'POST':
        post_stock_data.delay(country, ticker)
    elif request.method == 'PUT':
        put_stock_data.delay(country, ticker)
    elif request.method == 'DELETE':
        delete_stock_data.delay(country, ticker)
    return {'message': f'{country}의 {ticker or "전체"} 주식 데이터 갱신 요청이 시작되었습니다.'}, 202


@job_routes.route('/jobs/candles/<string:country>', methods=['POST', 'PUT', 'DELETE'])
@job_routes.route('/jobs/candles/<string:country>/<string:ticker>', methods=['POST', 'PUT', 'DELETE'])
def upsert_candle_data_route(country, ticker=None):
    if request.method == 'POST':
        post_candle_data.delay(country, ticker)
    elif request.method == 'PUT':
        put_candle_data.delay(country, ticker)
    elif request.method == 'DELETE':
        delete_candle_data.delay(country, ticker)
    return {'message': f'{country}의 {ticker or "전체"} 주식가 데이터 갱신 요청이 시작되었습니다.'}, 202
