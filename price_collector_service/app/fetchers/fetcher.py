from abc import ABC, abstractmethod


class Fetcher(ABC):
    @abstractmethod
    def fetch_data(self, ticker: str = None):
        pass

    @abstractmethod
    def sync_data(self, ticker: str = None):
        pass
