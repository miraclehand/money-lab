from abc import abstractmethod
from app.fetchers.fetcher import Fetcher


class DisclosureFetcher(Fetcher):
    @abstractmethod
    def sync_data(self, start_date: str = None, end_date: str = None):
        pass
