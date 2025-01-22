import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from yp_fin_utils.models import MarketModelFactory
from app.fetchers.fetcher_factory import FetcherFactory
from app.celery_app.worker import celery


logger = logging.getLogger(__name__)

@celery.task
def refresh_stock_data(country, ticker=None):
    delete_stock_data(country, ticker)
    sync_stock_data(country, ticker)

    return {'task':'stock post'}, 201

@celery.task
def sync_stock_data(country, ticker=None):
    stock_model = MarketModelFactory.get_model('STOCK', country)

    stock_fetcher = FetcherFactory.create_fetcher('STOCK', country)
    stock_fetcher.sync_data(ticker)

    today = datetime.now()
    two_months_ago = today - relativedelta(months=2)
    stock_model.objects.raw({'lastFetched':{'$lt':two_months_ago}}).update({'$set':{'crud':'D'}})

    return {'task':'stock put'}, 201

@celery.task
def delete_stock_data(country, ticker=None):
    stock_model = MarketModelFactory.get_model('STOCK', country)

    query = {'ticker': ticker} if ticker else {}
    stock_model.objects.raw(query).delete()

    return {'task':'stock delete'}, 201

