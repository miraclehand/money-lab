from datetime import datetime
from pymongo import ASCENDING
from pymongo.operations import IndexModel
from pymodm import fields, MongoModel
from yp_fin_utils.config.settings import CONNECTION_ALIAS


class Stock(MongoModel):
    country  = fields.CharField(required=True)
    code     = fields.CharField(required=True)
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
    lastUpdated = fields.DateTimeField()   # update if insert or delete code
    lastFetched = fields.DateTimeField()   # fetch everyday

    def __init__(self, newone=None, **kwargs):
        super().__init__(**kwargs)

        if newone is None:
            return
        self.country    = newone.get('country', '')
        self.code       = newone.get('code', '')
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
            'code': self.code,
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


class StockKR(Stock):
    class Meta:
        connection_alias = CONNECTION_ALIAS
        collection_name = 'stock_kr'
        indexes = [
            IndexModel([('code', ASCENDING)], name='stock_kr_code_index', unique=True)
        ]

    def __init__(self, newone=None, **kwargs):
        super().__init__(newone, **kwargs)

class StockUS(Stock):
    class Meta:
        connection_alias = CONNECTION_ALIAS
        collection_name = 'stock_us'
        indexes = [
            IndexModel([('code', ASCENDING)], name='stock_us_code_index', unique=True)
        ]

    def __init__(self, newone=None, **kwargs):
        super().__init__(newone, **kwargs)
