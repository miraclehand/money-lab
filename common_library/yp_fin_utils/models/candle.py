import os
from datetime import datetime
from pymodm import fields, MongoModel
from pymongo import ASCENDING
from pymongo.operations import IndexModel
from typing import Type, Union
from yp_fin_utils.config.settings import STOCKDB_ALIAS
from yp_fin_utils.models.stock import Stock, KRStock, USStock
from yp_fin_utils.models.ohlcv import Ohlcv


class Candle(MongoModel):
    stock = fields.ReferenceField(Stock, required=True)
    ohlcvs = fields.EmbeddedDocumentListField(Ohlcv, default=[])

    class Meta:
        abstract = True

    @classmethod
    def find_by_stock(self, stock_model, ticker):
        try:
            return stock_model.objects.raw({'ticker':ticker}).first()
        except Exception as e:
            return None

    @classmethod
    def find_by_stock_and_date(self, stock_instance, candle_model, start_date, end_date):
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date.replace('-',''), '%Y%m%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date.replace('-',''), '%Y%m%d')

        return candle_model.objects.raw({
            'stock': stock_instance._id,
        }).project({
            'stock': 1,  # stock 필드 유지
            'ohlcvs': {  # ohlcvs 배열 필터링
                '$filter': {
                    'input': '$ohlcvs',
                    'as': 'item',
                    'cond': {
                        '$and': [
                            { '$gte': ['$$item.date', start_date] },
                            { '$lte': ['$$item.date', end_date] }
                        ]
                    }
                }
            }
        })

    def update_ohlcv_with_adjustments(self, ohlcv_data_fetched):
        has_price_adjustment = False
        oldest_date_in_ohlcv_data_fetched = ohlcv_data_fetched[0]['date']

        for index, ohlcv in enumerate(self.ohlcvs):
            if ohlcv.date >= oldest_date_in_ohlcv_data_fetched:
                insert_position = index
                break

        # 과거 데이터 중 수정된 주가가 있는지 확인 (권리 처리 등)
        for idx, existing_ohlcv_data in enumerate(self.ohlcvs[insert_position:]):
            existing_date = existing_ohlcv_data.date
            existing_close_price = existing_ohlcv_data.close
    
            fetched_date = ohlcv_data_fetched[idx]['date']
            fetched_close_price = ohlcv_data_fetched[idx]['close']
    
            # 기존 데이터와 새 데이터의 종가(close)가 다르면 수정된 주가가 있다고 판단
            if existing_date == fetched_date and existing_close_price != fetched_close_price:
                has_price_adjustment = True
                break

        del self.ohlcvs[insert_position:]
        self.ohlcvs.extend([Ohlcv(ohlcv) for ohlcv in ohlcv_data_fetched])

        return has_price_adjustment

    @property
    def to_dict(self):
        return {
            'ticker': self.stock.ticker,
            'name': self.stock.name,
            'ohlcv': [ohlcv.to_dict for ohlcv in self.ohlcvs],
        }


class KRCandle(Candle):
    stock = fields.ReferenceField(KRStock, required=True)

    class Meta:
        connection_alias = STOCKDB_ALIAS
        collection_name = 'kr_candle'
        indexes = [
            IndexModel([('stock', ASCENDING)], name='kr_candle_stock_index', unique=True)
        ]


    @classmethod
    def find_by_stock(self, ticker):
        return super().find_by_stock(KRStock, ticker)

    @classmethod
    def find_by_stock_and_date(self, ticker, start_date, end_date):
        stock_instance = KRStock.objects.raw({'ticker':ticker}).first()
        return super().find_by_stock_and_date(stock_instance, self, start_date, end_date)

class USCandle(Candle):
    stock = fields.ReferenceField(USStock, required=True)

    class Meta:
        connection_alias = STOCKDB_ALIAS
        collection_name = 'us_candle'
        indexes = [
            IndexModel([('stock', ASCENDING)], name='us_candle_stock_index', unique=True)
        ]

    @classmethod
    def find_by_stock(self, ticker):
        return super().find_by_stock(USStock, ticker)

    @classmethod
    def find_by_stock_and_date(self, ticker, start_date, end_date):
        stock_instance = USStock.objects.raw({'ticker':ticker}).first()
        return super().find_by_stock_and_date(stock_instance, self, start_date, end_date)
