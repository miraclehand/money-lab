from abc import ABC, abstractmethod
from app.fetchers.fetcher import Fetcher


class CandleFetcher(Fetcher):
    @abstractmethod
    def fetch_data(self, ticker: str = None):
        pass

    @abstractmethod
    def sync_data(self, ticker: str = None, days: int = None):
        pass

    def get_previous_close(self, code: str, target_date, candle_model) -> float:
        """
        Retrieve the previous close price for a specific stock and date.

        Args:
            code (str): The stock code for which the data is being retrieved.
            target_date: The target date to find the previous close.
            candle_model: The model class representing the Candle data.

        Returns:
            float: The previous close price. Returns 0 if not found or data is unavailable.
        """
        try:
            # Fetch the Candle object for the given stock code
            candle = candle_model.objects.raw({'code': code}).first()
        except candle_model.DoesNotExist:
            # Return 0 if no Candle object is found
            return 0

        if not candle or not candle.ohlcvs:
            return 0

        # Locate the target date in OHLCVs
        ohlcvs = candle.ohlcvs
        for i, ohlcv in enumerate(ohlcvs):
            if ohlcv.date == target_date:
                return ohlcvs[i - 1].close if i > 0 else 0

        # Return 0 if target date not found
        return 0

    def calculate_price_changes(self, code: str, candle_model, ohlcvs: list) -> list:
        """
        Calculate the price difference and percentage change for each OHLCV entry.

        Args:
            code (str): The stock code for which the data is being processed.
            candle_model: The model class representing the Candle data.
            ohlcvs (list): List of OHLCV data dictionaries.

        Returns:
            list: Updated list of OHLCV data dictionaries with 'diff' and 'change' fields added.
        """
        previous_close = None

        for ohlcv in ohlcvs:
            if previous_close is None:
                # Fetch the previous close price for the first entry
                previous_close = self.get_previous_close(code, ohlcv['date'], candle_model)

            # Calculate price difference and percentage change
            price_diff = ohlcv['close'] - previous_close
            percentage_change = (price_diff / previous_close * 100) if previous_close != 0 else 0

            # Update the OHLCV data
            ohlcv['diff'] = price_diff
            ohlcv['change'] = percentage_change

            # Update the previous close for the next iteration
            previous_close = ohlcv['close']

        return ohlcvs
