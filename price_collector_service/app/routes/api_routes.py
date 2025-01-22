from flask import Blueprint
from yp_fin_utils.models import MarketModelFactory


api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/stocks/<string:country>', methods=['GET'])
@api_routes.route('/api/stocks/<string:country>/<string:ticker>', methods=['GET'])
def query_stock_data_route(country, ticker: str = None):
    stock_model = MarketModelFactory.get_model('STOCK', country)

    query = {'crud': {'$ne': 'D'}}
    if ticker:
        query['ticker'] = ticker

    stock_query = stock_model.objects.raw(query)
    stocks = [stock.to_dict for stock in stock_query]

    return {'stocks': stocks}

@api_routes.route('/api/candles/<string:country>/<string:ticker>', methods=['GET'])
@api_routes.route('/api/candles/<string:country>/<string:ticker>/<string:start_date>/<string:end_date>', methods=['GET'])
def query_candle_data_route(country, ticker, start_date: str = None, end_date: str = None):
    if not start_date:
        start_date = '1000-01-01'
    if not end_date:
        end_date = '9999-12-31'
    candle_query = MarketModelFactory.find_candle_by_ticker_and_date_range(country, ticker, start_date, end_date)
    candles = [candle.to_dict for candle in candle_query]

    return {'candles': candles}
