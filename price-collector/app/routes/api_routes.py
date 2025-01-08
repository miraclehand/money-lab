from flask import Blueprint
from yp_fin_utils.models.stock import get_stock_model
from yp_fin_utils.models.candle import get_candle_model


api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/stocks/<string:country>/<string:ticker>', methods=['GET'])
def query_stock_data_route(country, ticker):
    StockModel = get_stock_model(country)

    query = {'crud': {'$ne': 'D'}}
    if ticker:
        query['ticker'] = ticker

    stock_query = StockModel.objects.raw(query)
    stocks = [stock.to_dict for stock in stock_query]

    return {'stocks':stocks}

@api_routes.route('/api/candles/<string:country>/<string:ticker>', methods=['GET'])
@api_routes.route('/api/candles/<string:country>/<string:ticker>/<string:start_date>/<string:end_date>', methods=['GET'])
def query_candle_data_route(country, ticker, start_date=None, end_date=None):
    CandleModel = get_candle_model(country)
    candle_query = CandleModel.find_by_stock_and_date(ticker, start_date, end_date)
    candles = [candle.to_dict for candle in candle_query]

    return {'candles':candles}
