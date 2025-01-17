import asyncio
import logging
import math
import numpy as np
from datetime import datetime
from aiohttp import ClientSession
from pymodm import MongoModel
from pymodm.errors import DoesNotExist
from yp_fin_utils.parsers.parsers import extract_between_markers
from yp_fin_utils.models import MarketModelFactory
from app.fetchers.candle_fetcher import CandleFetcher


logger = logging.getLogger(__name__)

class KRCandleFetcher(CandleFetcher):
    def __init__(self):
        super(CandleFetcher, self).__init__()

        self.COUNTRY = 'KR'
        self.DAYS = 3650  # 10 years of data
        self.BATCH_SIZE = 100
        self.BASE_URL = 'https://fchart.stock.naver.com/sise.nhn?symbol={ticker}&timeframe=day&count={days}&requestType=0'
        self.stock_model = MarketModelFactory.get_model('STOCK', self.COUNTRY)
        self.candle_model = MarketModelFactory.get_model('CANDLE', self.COUNTRY)
        self.ohlcv_model = MarketModelFactory.get_model('OHLCV', self.COUNTRY)

    def fetch_data(self, ticker: str = None):
        pass

    async def _fetch_ohlcv_async(self, url):
        ticker = extract_between_markers(url, 'symbol=', '&')

        async with ClientSession() as session:
            async with session.get(url) as response:
                await asyncio.sleep(0.1)  # Rate limiting
                html = await response.read()
                html = html.decode('euc-kr', 'ignore').replace('\t', '').replace('"', '').replace('/>', '')
                return self._parse_ohlcv_data(ticker, html)

    def _parse_ohlcv_data(self, ticker, html):
        ohlcvs = []

        for line in html.split('\n'):
            line = line.strip().replace('"', '')
            if not line.startswith('<item data='):
                continue

            value = line.replace('<item data=', '').replace('/>', '').split('|')
            if len(value) < 6:
                continue

            date, open_, high, low, close, volume = value[:6]
            try:
                ohlcvs.append({
                    'ticker': ticker,
                    'date': datetime.strptime(date, '%Y%m%d'),
                    'open': int(open_),
                    'high': int(high),
                    'low': int(low),
                    'close': int(close),
                    'volume': int(volume),
                    'log': math.log(int(close))
                })
            except (ValueError, IndexError):
                continue
        return ohlcvs

    def sync_data(self, ticker: str = None, days: int = None):
        query = {'ticker': ticker} if ticker else {}
        stocks = self.stock_model.objects.raw(query).order_by([('capital', -1)])
        total_stocks = stocks.count()

        if not days:
            days = self.DAYS

        logger.info(f"Fetching candle data for {total_stocks} stocks")

        for start in range(0, total_stocks, self.BATCH_SIZE):
            end = min(start + self.BATCH_SIZE, total_stocks)

            logger.info(f"Processing batch {start + 1} to {end} for {total_stocks}")
            batch_stocks = stocks[start:end]

            urls = [self.BASE_URL.format(ticker=stock.ticker, days=days) for stock in batch_stocks]
            ohlcv_data_fetched = self._fetch_ohlcv_data_async(urls)

            stock_instance_map = {stock.ticker: stock for stock in batch_stocks}

            for ohlcv_data in ohlcv_data_fetched:
                if ohlcv_data:
                    enhanced_ohlcv_data = self.calculate_price_changes(ticker, self.candle_model, ohlcv_data)
                    self._upsert_candle_data(enhanced_ohlcv_data, stock_instance_map)

    def _fetch_ohlcv_data_async(self, urls: list) -> list:
        """
        Fetch OHLCV data asynchronously for the given URLs.
        """
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

        tasks = [asyncio.ensure_future(self._fetch_ohlcv_async(url)) for url in urls]
        ohlcv_data_fetched = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()

        return ohlcv_data_fetched

    def _upsert_candle_data(self, ohlcv_data: list,  stock_instance_map: dict):
        """
        Save the fetched OHLCV data to the database.
        """
        ticker = ohlcv_data[0]['ticker']
        stock_instance = stock_instance_map.get(ticker)

        try:
            candle = self.candle_model.objects.get({'stock':stock_instance._id})
            stock_instance.new_adj_close = candle.update_ohlcv_with_adjustments(ohlcv_data)
            candle.save()
        except DoesNotExist:
            candle = self.candle_model(
                stock=stock_instance,
                ohlcvs=[self.ohlcv_model(ohlcv) for ohlcv in ohlcv_data]
            )
            candle.save()
            stock_instance.new_adj_close = False

        recent_ohlcvs = candle.ohlcvs[-50:]
        stock_instance.avg_v50 = np.average([ohlcv.close * ohlcv.volume for ohlcv in recent_ohlcvs])
        stock_instance.save()
