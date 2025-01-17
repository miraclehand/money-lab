from abc import abstractmethod
from app.fetchers.kr_dividend_disclosure_fetcher import KRDividendDisclosureFetcher


class FetcherFactory:
    @staticmethod
    def create_fetcher(disclosure_type: str, country: str):
        disclosure_type = disclosure_type.upper()
        country = country.upper()

        if country == "KR":
            if disclosure_type == 'DIVIDEND':
                return KRDividendDisclosureFetcher()
            else:
                raise Exception(f"Unsupported disclosure_type: {disclosure_type}")
        else:
            raise Exception(f"Unsupported country: {country}")
