from flask_restful import Resource
from typing import Type, Union
from yp_fin_utils.models.candle import CandleKR, CandleUS
from app.utils.logging import log_request


class CandleDataResource(Resource):
    CANDLE_MODELS = {
        'kr': CandleKR,
        'us': CandleUS
    }

    def __init__(self):
        super(CandleDataResource, self).__init__()

    def _get_candle_model(self, country: str) -> Type[Union[CandleKR, CandleUS]]:
        model = self.CANDLE_MODELS.get(country.lower())
        if not model:
            raise ValueError(f"Unsupported country code: {country}")
        return model

    @log_request('get candle')
    def get(self, country=None, id=None, date1=None, date2=None):

        CandleModel = self._get_candle_model(country)

        if not id:
            return {'candle': 'None'}

        candle = CandleModel.objects.get({'code':id})

        return {'candle':to_json(candle.to_dict)}

    @log_request('put candle')
    def put(self, country=None, id=None):
        print('put candle', cntry, id)

        #put_candle.delay(cntry, id)

        return {'task':'candle put'}, 201

    @log_request('post candle')
    def post(self, country=None, id=None):

        #post_candle.delay(cntry, id)

        return {'task':'candle post'}, 201

    @log_request('delete candle')
    def delete(self, country=None, id=None):

        #del_candle.delay(cntry, id)

        return {'task':'candle delete'}, 201

