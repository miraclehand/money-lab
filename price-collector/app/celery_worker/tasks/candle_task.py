import logging
from yp_fin_utils.models.stock import get_stock_model
from yp_fin_utils.models.candle import get_candle_model
from app.services.fetchers.fetcher_factory import FetcherFactory
from app.celery_worker.worker import celery


logger = logging.getLogger(__name__)

@celery.task
def post_candle_data(country, ticker=None):
    CandleModel = get_candle_model(country)
    stock_instance = CandleModel.find_by_stock(ticker)

    query = {'stock': stock_instance._id} if stock_instance else {}
    CandleModel.objects.raw(query).delete()

    candle_fetcher = FetcherFactory.create_fetcher('CANDLE', country)
    candle_fetcher.fetch_and_upsert_candle_data(ticker)

    return {'task':'candle post'}, 201

@celery.task
def put_candle_data(country, ticker=None):
    logger.info(f"put_candle_data")
    logger.info(f"put_candle_data")
    logger.info(f"put_candle_data {country}, {ticker}")
    CandleModel = get_candle_model(country)
    stock_instance = CandleModel.find_by_stock(ticker)

    days = 14 # 2weeks
    candle_fetcher = FetcherFactory.create_fetcher('CANDLE', country)
    candle_fetcher.fetch_and_upsert_candle_data(ticker, days)

    StockModel = get_stock_model(country)
    stocks = StockModel.objects.raw({'new_adj_close':True})

    total_stocks = stocks.count()
    for index, stock_instance in enumerate(stocks):
        logger.info(f"{stock_instance}, {index} / {total_stocks}")
        StockModel.objects.raw({'_id':stock_instance._id}).update({'$set':{'new_adj_close':False}})

        query = {'stock': stock_instance._id} if stock_instance else {}
        CandleModel.objects.raw(query).delete()
        candle_fetcher.fetch_and_upsert_candle_data(stock_instance.ticker)

    return {'task':'candle put'}, 201

@celery.task
def delete_candle_data(country, ticker=None, start_date=None, end_date=None):
    CandleModel = get_candle_model(country)
    stock_instance = CandleModel.find_by_stock(ticker)

    query = {'stock': stock_instance._id} if stock_instance else {}
    CandleModel.objects.raw(query).delete()

    return {'task':'candle delete'}, 201
