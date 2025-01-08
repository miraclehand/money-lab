from .stock_fetcher_kr import StockFetcherKR
from .candle_fetcher_kr import CandleFetcherKR


class FetcherFactory:
    @staticmethod
    def create_fetcher(data_type: str, country: str):
        data_type = data_type.upper()
        country = country.upper()

        if country == "KR":
            if data_type == "STOCK":
                return StockFetcherKR()
            elif data_type == "CANDLE":
                return CandleFetcherKR()
        else:
            raise Exception(f"Unsupported country: {country}")
