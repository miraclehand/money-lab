import os
from datetime import datetime
from pymodm import fields, MongoModel
from pymongo import ASCENDING
from pymongo.operations import IndexModel
from yp_fin_utils.models.stock import Stock, KRStock
from yp_fin_utils.models.candle import Candle, KRCandle
from yp_fin_utils.config.settings import STOCKDB_ALIAS
from yp_fin_utils.utils.utils import formatted_date


class Disclosure(MongoModel):
    country   = fields.CharField(required=True)
    recept_dt = fields.CharField(required=True)
    recept_no = fields.CharField(required=True)
    recept_nm = fields.CharField(required=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)

    stock  = fields.ReferenceField(Stock, required=True)
    candle = fields.ReferenceField(Candle, required=True)

    class Meta:
        abstract = True

class DividendDisclosure(Disclosure):
    country = fields.CharField(required=True)
    dividend_type   = fields.CharField(blank=True)
    dividend_method = fields.CharField(blank=True)
    asset_details = fields.CharField(blank=True)
    total_dividend_amount = fields.IntegerField(blank=True)
    record_date = fields.CharField(blank=True)
    payment_date = fields.CharField(blank=True)

    class Meta:
        abstract = True

    def __init__(self, country=None, stock_id=None, candle_id=None, newone=None, **kwargs):
        super().__init__(**kwargs)

        if not all([country, stock_id, candle_id, newone]):
            return

        self.country = country
        self.stock = stock_id
        self.candle = candle_id

        self.recept_dt = formatted_date(newone.get('rcept_dt', ''))
        self.recept_no = newone.get('rcept_no', '')
        self.recept_nm = newone.get('report_nm', '')
        self.dividend_type = newone.get('dividend_type', '')
        self.dividend_method = newone.get('dividend_method', '')
        self.asset_details = newone.get('asset_details', '')
        self.total_dividend_amount = newone.get('total_dividend_amount', '')
        self.record_date = formatted_date(newone.get('record_date', ''))
        self.payment_date = formatted_date(newone.get('payment_date', ''))
        self.updated_at = datetime.now().date()

class KRDividendDisclosure(DividendDisclosure):
    stock  = fields.ReferenceField(KRStock, required=True)
    candle = fields.ReferenceField(KRCandle, required=True)

    class Meta:
        connection_alias = STOCKDB_ALIAS
        collection_name = 'kr_dividend_disclosure'
        indexes = [
            IndexModel([('stock', ASCENDING)], name='stock_idx'),
            IndexModel([('recept_dt', ASCENDING)], name='recept_dt_idx'),
            IndexModel([('record_date', ASCENDING)], name='record_date_idx'),
        ]

    def __init__(self, country=None, stock_id=None, candle_id=None, newone=None, **kwargs):
        super().__init__(country, stock_id, candle_id, newone, **kwargs)
