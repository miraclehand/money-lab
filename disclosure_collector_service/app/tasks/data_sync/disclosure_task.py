import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from yp_fin_utils.utils.utils import formatted_date
from yp_fin_utils.models import MarketModelFactory
from app.fetchers.fetcher_factory import FetcherFactory
from app.celery_app.worker import celery


logger = logging.getLogger(__name__)

@celery.task
def refresh_disclosure_data(country, disclosure_type, start_date: str = None, end_date: str = None):
    delete_disclosure_data(country, disclosure_type, start_date, end_date)
    sync_disclosure_data(country, disclosure_type, start_date, end_date)
    return {'task':'stock post'}, 201

@celery.task
def sync_disclosure_data(country, disclosure_type, start_date: str = None, end_date: str = None):
    disclosure_fetcher = FetcherFactory.create_fetcher('DIVIDEND', country)
    disclosure_fetcher.sync_data(start_date, end_date)

    return {'task':'stock put'}, 201

@celery.task
def delete_disclosure_data(country, disclosure_type, start_date='10000101', end_date='99991231'):
    query = {}
    if start_date:
        query['recept_dt__gte'] = formatted_date(start_date)
    if end_date:
        query['recept_dt__lte'] = formatted_date(end_date)

    disclosure_model = MarketModelFactory.get_model('DISCLOSURE', country)
    disclosure_model.objects.raw(query).delete()

    return {'task':'stock delete'}, 201
