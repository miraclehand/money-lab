from abc import ABC, abstractmethod

class StockFetcher(ABC):
    @abstractmethod
    def fetch_stock_data(self):
        pass

    @abstractmethod
    def fetch_and_upsert_stock_data(self, ticker):
        pass
