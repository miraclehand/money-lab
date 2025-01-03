from abc import ABC, abstractmethod

class OHLCVFetcher(ABC):
    @abstractmethod
    def fetch_ohlcv_data(self, stock_code: str, start_date: str, end_date: str):
        pass

