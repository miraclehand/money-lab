from abc import abstractmethod
from app.fetchers.fetcher import Fetcher


class StockFetcher(Fetcher):
    @abstractmethod
    def fetch_data(self, ticker: str = None):
        pass

    @abstractmethod
    def sync_data(self, ticker: str = None, days: int = None):
        pass
