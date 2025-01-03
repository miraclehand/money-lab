import os
from pymodm import fields, MongoModel
from pymongo import ASCENDING
from pymongo.operations import IndexModel
from .stock import Stock
from .ohlcv import Ohlcv
from yp_fin_utils.config.settings import CONNECTION_ALIAS


class Candle(MongoModel):
    code = fields.CharField(required=True)
    stock = fields.ReferenceField(Stock, required=True)
    ohlcvs = fields.EmbeddedDocumentListField(Ohlcv, default=[])

    def add_or_replace_ohlcv(self, ohlcvs):
        new_adj_close = False
        for i, ohlcv in enumerate(self.ohlcvs):
            if ohlcv.date >= ohlcvs[0]['date']:
                break

        # 권리 때문에, 과거의 수정주가가 바뀌는 경우가 있으면
        # 과거 주가를 다시 받아야한다
        for idx, o in enumerate(self.ohlcvs[i:]):
            #당일 데이터는 무조건 새로운 데이터
            if ohlcvs[idx] == ohlcvs[-1]:
                break
            if o.close != ohlcvs[idx]['close']:
                new_adj_close = True
                break;
        del self.ohlcvs[i:]
        self.ohlcvs.extend([Ohlcv(ohlcv['date'],ohlcv) for ohlcv in ohlcvs])
        return new_adj_close

    def add_or_replace_ohlcv_dict(self, ohlcvs):
        for i, ohlcv in enumerate(self.ohlcvs):
            if ohlcv.date >= ohlcvs.index[-1].to_pydatetime():
                break

        if i > 0:
            del self.ohlcvs[i:]
            self.ohlcvs.extend([Ohlcv(date, ohlcv) for date, ohlcv in ohlcvs.iterrows()])


    def get_close(self, date):
        ohlcv = list(filter(lambda ohlcv: ohlcv.date == date, self.ohlcvs))
        if not ohlcv:
            return 0;
        if ohlcv.__len__() != 1:
            return 0;
        return ohlcv[0].close

    @property
    def to_dict(self):
        return {
            'code'  : self.stock.code,
            'name'  : self.stock.name,
            'ohlcv' : list(self.ohlcvs),
        }


class CandleKR(Candle):
    stock = fields.ReferenceField(StockKR, required=True)

    class Meta:
        connection_alias = CONNECTION_ALIAS
        collection_name = 'candle_kr'
        indexes = [
            IndexModel([('code', ASCENDING)], name='candle_kr_code_index',unique=True)
        ]


class CandleUS(Candle):
    stock = fields.ReferenceField(StockUS, required=True)

    class Meta:
        connection_alias = CONNECTION_ALIAS
        collection_name = 'candle_us'
        indexes = [
            IndexModel([('code', ASCENDING)], name='candle_us_code_index',unique=True)
        ]
