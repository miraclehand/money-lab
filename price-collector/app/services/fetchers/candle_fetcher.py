from abc import ABC, abstractmethod

class CandleFetcher(ABC):
    @abstractmethod
    def fetch_candle_data(self, stock_code: str, start_date: str, end_date: str):
        pass

