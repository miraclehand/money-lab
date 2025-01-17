from datetime import datetime
from pymongo import ASCENDING
from pymongo.operations import IndexModel
from pymodm import fields, MongoModel
from typing import Type, Union
from yp_fin_utils.config.settings import STOCKDB_ALIAS


class Stock(MongoModel):
    country  = fields.CharField(required=True)
    ticker   = fields.CharField(required=True)
    name     = fields.CharField(required=True)
    dname    = fields.CharField(required=True)  # disassembled name
    label    = fields.CharField(required=True)
    exchange = fields.CharField()
    group_name = fields.CharField()
    sector   = fields.CharField()
    industry = fields.CharField()
    aimed    = fields.CharField()
    capital  = fields.IntegerField()
    avg_v50  = fields.IntegerField()    #average trading value during 50days
    new_adj_close = fields.BooleanField()
    crud     = fields.CharField()   #create, read, update, delete
    lastUpdated = fields.DateTimeField()   # update if insert or delete ticker
    lastFetched = fields.DateTimeField()   # fetch everyday

    class Meta:
        abstract = True

    def __init__(self, newone=None, **kwargs):
        super().__init__(**kwargs)

        if newone is None:
            return
        self.country    = newone.get('country', '')
        self.ticker     = newone.get('ticker', '')
        self.name       = newone.get('name', '')
        self.dname      = newone.get('dname', '')
        self.label      = newone.get('label', '')
        self.exchange   = newone.get('exchange', '')
        self.group_name = newone.get('group_name', '')
        self.sector     = newone.get('sector', '')
        self.industry   = newone.get('industry', '')
        self.capital    = newone.get('capital', '')
        self.avg_v50    = newone.get('avg_v50', '')
        self.crud       = 'C'
        self.new_adj_close = False
        today = datetime.now().date()
        self.lastUpdated  = today
        self.lastFetched  = today

    @property
    def to_dict(self):
        return {
            'id'  : str(self._id),
            'country': self.country,
            'ticker': self.ticker,
            'name': self.name,
            'dname': self.dname,
            'label': self.label,
            'exchange': self.exchange,
            'group_name': self.group_name,
            'sector': self.sector,
            'industry': self.industry,
            'capital': self.capital,
            'avg_v50': self.avg_v50,
            'crud': self.crud,
            'lastUpdated': self.lastUpdated.date().isoformat(),
            'lastFetched': self.lastFetched.date().isoformat(),
        }


class KRStock(Stock):
    class Meta:
        connection_alias = STOCKDB_ALIAS
        collection_name = 'kr_stock'
        indexes = [
            IndexModel([('ticker', ASCENDING)], name='kr_stock_ticker_index', unique=True)
        ]

    def __init__(self, newone=None, **kwargs):
        super().__init__(newone, **kwargs)

class USStock(Stock):
    class Meta:
        connection_alias = STOCKDB_ALIAS
        collection_name = 'us_stock'
        indexes = [
            IndexModel([('ticker', ASCENDING)], name='us_stock_ticker_index', unique=True)
        ]

    def __init__(self, newone=None, **kwargs):
        super().__init__(newone, **kwargs)
