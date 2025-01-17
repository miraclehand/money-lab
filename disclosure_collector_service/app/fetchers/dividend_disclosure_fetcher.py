from app.fetchers.disclosure_fetcher import DisclosureFetcher


class DividendDisclosureFetcher(DisclosureFetcher):
    @abstractmethod
    def sync_data(self, start_date: str = None, end_date: str = None):
        pass
