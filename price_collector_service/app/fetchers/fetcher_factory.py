from app.fetchers.kr_stock_fetcher import KRStockFetcher
from app.fetchers.kr_candle_fetcher import KRCandleFetcher


class FetcherFactory:
    @staticmethod
    def create_fetcher(data_type: str, country: str):
        data_type = data_type.upper()
        country = country.upper()

        if country == "KR":
            if data_type == "STOCK":
                return KRStockFetcher()
            elif data_type == "CANDLE":
                return KRCandleFetcher()
        else:
            raise Exception(f"Unsupported country: {country}")
