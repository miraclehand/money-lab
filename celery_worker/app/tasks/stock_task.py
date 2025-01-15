import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from yp_fin_utils.models.stock import get_stock_model
from services.fetchers.fetcher_factory import FetcherFactory
from app.worker import celery


logger = logging.getLogger(__name__)

@celery.task
def post_stock_data(country, ticker=None):
    StockModel = get_stock_model(country)
    StockModel.objects.delete()

    stock_fetcher = FetcherFactory.create_fetcher('STOCK', country)
    stock_fetcher.fetch_and_upsert_stock_data(ticker)

    return {'task':'stock post'}, 201

@celery.task
def put_stock_data(country, ticker=None):
    StockModel = get_stock_model(country)

    stock_fetcher = FetcherFactory.create_fetcher('STOCK', country)
    stock_fetcher.fetch_and_upsert_stock_data(ticker)

    today = datetime.now()
    two_months_ago = today - relativedelta(months=2)
    StockModel.objects.raw({'lastFetched':{'$lt':two_months_ago}}).update({'$set':{'crud':'D'}})

    return {'task':'stock put'}, 201

@celery.task
def delete_stock_data(country, ticker=None):
    query = dict()
    if ticker:
        query['ticker'] = ticker

    StockModel = get_stock_model(country)
    StockModel.objects.raw(query).delete()

    return {'task':'stock delete'}, 201
