from flask_restful import Resource
from typing import Type, Union
from yp_fin_utils.models.stock import StockKR, StockUS
from app.utils.logging import log_request
from app.services.fetchers.fetcher_factory import FetcherFactory


class StockDataResource(Resource):
    STOCK_MODELS = {
        'kr': StockKR,
        'us': StockUS
    }

    def __init__(self):
        super(StockDataResource, self).__init__()


    def _get_stock_model(self, country: str) -> Type[Union[StockKR, StockUS]]:
        model = self.STOCK_MODELS.get(country.lower())
        if not model:
            raise ValueError(f"Unsupported country code: {country}")
        return model

    @log_request('get stocks')
    def get(self, country: str = 'kr', id: str = None) -> dict:
        StockModel = self._get_stock_model(country)

        query = {'crud': {'$ne': 'D'}}
        if id:
            query['code'] = id

        stocks_query = StockModel.objects.raw(query)
        stocks = [stock.to_dict for stock in stocks_query]

        return {'stocks':stocks}

    @log_request('put stocks')
    def put(self, country=None, id: str = None) -> tuple:
        #TODO

        return {'task':'stock put'}, 201

    @log_request('post stocks')
    def post(self, country: str = None, id: str = None) -> tuple:
        StockModel = self._get_stock_model(country)
        StockModel.objects.delete()

        stock_fetcher = FetcherFactory.create_fetcher('STOCK', country)
        stock_fetcher.fetch_stock_data_then_save()

        return {'task':'stock post'}, 201

    @log_request('delete stocks')
    def delete(self, country: str = None, id: str = None) -> tuple:
        query = dict()
        if id:
            query['code'] = id

        StockModel = self._get_stock_model(country)
        StockModel.objects.raw(query).delete()

        return {'task':'stock delete'}, 201

