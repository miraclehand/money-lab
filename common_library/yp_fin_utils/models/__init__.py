from yp_fin_utils.models.stock  import KRStock,  USStock
from yp_fin_utils.models.candle import KRCandle, USCandle
from yp_fin_utils.models.ohlcv import Ohlcv
from yp_fin_utils.models.disclosure import KRDividendDisclosure


MODEL_REGISTRY = {
    'STOCK': {
        'KR': KRStock,
        'US': USStock,
    },
    'CANDLE': {
        'KR': KRCandle,
        'US': USCandle,
    },
    'OHLCV': {
        'ALL': Ohlcv,
    },
    'DISCLOSURE': {
        'KR': KRDividendDisclosure,
    },
}

class MarketModelFactory:
    @staticmethod
    def get_model(market_type: str, country: str):
        market_type = market_type.upper()
        country = country.upper()

        market_models = MODEL_REGISTRY.get(market_type)
        if not market_models:
            raise ValueError(f"Unsupported market type: {market_type}. Supported types: {list(MODEL_REGISTRY.keys())}")

        market_model = market_models.get(country) or market_models.get('ALL')

        if not market_model:
            raise ValueError(f"Unsupported country code for {market_type}: {country}")

        return market_model

    @staticmethod
    def find_stock_by_ticker(country: str, ticker: str):
        stock_model = MarketModelFactory.get_model('STOCK', country)
        stock_cursor = stock_model.objects.raw({'ticker': ticker})
        return stock_cursor.first() if stock_cursor.count() > 0 else None

    @staticmethod
    def find_related_candle_by_stock(country: str, stock_instance):
        if not stock_instance:
            raise ValueError("Stock instance is required.")

        model = MarketModelFactory.get_model('CANDLE', country)
        cursor = model.objects.raw({'stock': stock_instance._id})
        return cursor.first() if cursor.count() > 0 else None

    @staticmethod
    def find_candle_by_ticker(country: str, ticker: str):
        candle_model = CANDLE_MODELS.get(country)
        if not candle_model:
            raise ValueError(f"Unsupported country code: {country}")

        stock = find_stock_by_ticker(country, ticker)
        if not stock:
            return None

        candle = find_candle_by_stock(country, stock)
        return candle

    @staticmethod
    def find_candle_by_ticker(country: str, ticker: str):
        stock = MarketModelFactory.find_stock_by_ticker(country, ticker)
        if not stock:
            return None

        return MarketModelFactory.find_related_candle_by_stock(country, stock)
