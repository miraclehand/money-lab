from abc import ABC, abstractmethod

class StockFetcher(ABC):
    @abstractmethod
    def fetch_stock_data(self, stock_code: str):
        pass

