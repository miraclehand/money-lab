import logging
from yp_fin_utils.models import MarketModelFactory
from app.fetchers.fetcher_factory import FetcherFactory
from app.celery_app.worker import celery


logger = logging.getLogger(__name__)

@celery.task
def refresh_candle_data(country, ticker=None):
    delete_candle_data(country, ticker)

    candle_fetcher = FetcherFactory.create_fetcher('CANDLE', country)
    candle_fetcher.sync_data(ticker)

    return {'task':'candle post'}, 201

@celery.task
def sync_candle_data(country, ticker=None):
    candle_model = MarketModelFactory.get_model('CANDLE', country)

    days = 14 # 2weeks
    candle_fetcher = FetcherFactory.create_fetcher('CANDLE', country)
    candle_fetcher.sync_data(ticker, days)

    stock_model = MarketModelFactory.get_model('STOCK', country)
    stocks = stock_model.objects.raw({'new_adj_close':True})

    total_stocks = stocks.count()
    for index, stock_instance in enumerate(stocks):
        logger.info(f"{stock_instance}, {index} / {total_stocks}")
        stock_model.objects.raw({'_id':stock_instance._id}).update({'$set':{'new_adj_close':False}})

        query = {'stock': stock_instance._id} if stock_instance else {}
        candle_model.objects.raw(query).delete()
        candle_fetcher.sync_data(stock_instance.ticker)

    return {'task':'candle put'}, 201

@celery.task
def delete_candle_data(country, ticker=None, start_date=None, end_date=None):
    candle_model = MarketModelFactory.get_model('CANDLE', country)
    stock_instance = MarketModelFactory.find_stock_by_ticker(country, ticker)

    query = {'stock': stock_instance._id} if stock_instance else {}
    candle_model.objects.raw(query).delete()

    return {'task':'candle delete'}, 201
