from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class Fetcher(ABC):
    @abstractmethod
    def sync_data(self, start_date: str, end_date: str):
        pass

    def calculate_date_range(self, start_date: str = None, end_date: str = None):
        today = datetime.today()
        today_str = today.strftime('%Y%m%d')

        seven_days_ago = today - timedelta(days=7)

        start_date_str = start_date.replace('-','') if start_date else seven_days_ago.strftime('%Y%m%d')
        end_date_str = end_date.replace('-','') if end_date else today_str

        return start_date_str, end_date_str
