from flask_restful import Api
from app.resources.stock import StockDataResource
from app.resources.candle import CandleDataResource


def register_api_routes(app):
    api = Api(app)

    api.add_resource(StockDataResource,  '/api/stocks/<string:country>',
                                         '/api/stocks/<string:country>/<string:id>',
                                         endpoint='stock')
    api.add_resource(CandleDataResource, '/api/candles/<string:country>',
                                         '/api/candles/<string:country>/<string:id>',
                                         endpoint='candle')
