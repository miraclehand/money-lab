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

    def calculate_average_weighted_close(self, target_date, days=20):
        if isinstance(target_date, str):
            target_date = datetime.strptime(target_date.replace('-', ''), '%Y%m%d')

        filtered_ohlcvs = [ohlcv for ohlcv in self.ohlcvs if ohlcv.date <= target_date]
        recent_ohlcvs = filtered_ohlcvs[-days:]
        weighted_sum = sum(ohlcv.close * ohlcv.volume for ohlcv in recent_ohlcvs)
        return weighted_sum / days if filtered_ohlcvs else 0.0

    def get_ohlcv(self, date):
        if isinstance(date, str):
            date = datetime.strptime(date.replace('-',''), '%Y%m%d')

        ohlcv = [o for o in self.ohlcvs if o.date == date]
        return ohlcv[0]

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
            IndexModel([('stock', ASCENDING)], name='kr_candle_stock_index', unique=True),
            IndexModel([('stock', ASCENDING), ('ohlcvs.date', ASCENDING)], name='kr_candle_ohlcv_index', unique=True)
        ]
    def calculate_average_weighted_close__(self, candle_model, target_date: Union[str, datetime], days: int = 20) -> float:
        if isinstance(target_date, str):
            target_date = datetime.strptime(target_date.replace('-', ''), '%Y%m%d')

        pipeline = [
            {
                '$match': {
                    '_id': self._id
                }
            },
            {
                '$project': {
                    'ohlcvs': {
                        '$filter': {
                            'input': '$ohlcvs',
                            'as': 'ohlcv',
                            'cond': {'$lte': ['$$ohlcv.date', target_date]}
                        }
                    }
                }
            },
            {
                '$project': {
                    'last_n_ohlcvs': {
                        '$slice': ['$ohlcvs', -days]
                    }
                }
            },
            {
                '$unwind': '$last_n_ohlcvs'
            },
            {
                '$group': {
                    '_id': None,
                    'weighted_sum': {
                        '$sum': {
                            '$multiply': ['$last_n_ohlcvs.close', '$last_n_ohlcvs.volume']
                        }
                    },
                    'count': {'$sum': 1}
                }
            }
        ]

        result = list(self.objects.aggregate(pipeline))
        
        if not result:
            return 0.0
            
        weighted_sum = result[0]['weighted_sum']
        count = result[0]['count']
        
        return weighted_sum / days if count > 0 else 0.0

class USCandle(Candle):
    stock = fields.ReferenceField(USStock, required=True)

    class Meta:
        connection_alias = STOCKDB_ALIAS
        collection_name = 'us_candle'
        indexes = [
            IndexModel([('stock', ASCENDING)], name='us_candle_stock_index', unique=True),
            IndexModel([('stock', ASCENDING), ('ohlcvs.date', ASCENDING)], name='us_candle_ohlcv_index', unique=True)
        ]
