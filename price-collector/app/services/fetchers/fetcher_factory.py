from .stock_fetcher_kr import StockFetcherKR
from .ohlcv_fetcher_kr import OHLCVFetcherKR
from .candle_fetcher_kr import CandleFetcherKR
#from .stock_fetcher_us import StockFetcherUS
#from .ohlcv_fetcher_us import OHLCVFetcherUS
#from .candle_fetcher_us import CandleFetcherUS

class FetcherFactory:
    @staticmethod
    def create_fetcher(data_type: str, country: str):
        data_type = data_type.upper()
        country = country.upper()

        if country == "KR":
            if data_type == "STOCK":
                return StockFetcherKR()
            elif data_type == "OHLCV":
                return OHLCVFetcherKR()
            elif data_type == "CANDLE":
                return CandleFetcherKR()
        #elif country == "US":
        #    if data_type == "STOCK":
        #        return StockFetcherUs()
        #    elif data_type == "OHLCV":
        #        return OHLCVFetcherUS()
        #    elif data_type == "CANDLE":
        #        return CandleFetcherUs()
        else:
            raise Exception(f"Unsupported country: {country}")
