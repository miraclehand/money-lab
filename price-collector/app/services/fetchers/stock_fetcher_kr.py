import requests
import re
import asyncio
import aiohttp
from yp_fin_utils.parsers.parsers import get_value_from_text
from yp_fin_utils.utils.utils import disassemble_hangul
from yp_fin_utils.models.stock import StockKR
from .stock_fetcher import StockFetcher


class StockFetcherKR(StockFetcher):
    def __init__(self, base_url: str = 'https://finance.naver.com'):
        self.base_url = base_url
        self.group_stocks = {}

    def fetch_stock_group(self):
        group_url = f"{self.base_url}/sise/sise_group.nhn?type=group"
        response = requests.get(group_url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch stock groups: {response.status_code}")

        group_ids = self._extract_group_ids(response.text)
        detail_urls = self._create_detail_urls(group_ids)

        return self._fetch_group_stocks(detail_urls)

    def _extract_group_ids(self, html_text: str) -> list:
        group_id_pattern = r'/sise/sise_.*group&no=([0-9]+)'
        return re.findall(group_id_pattern, html_text)

    def _create_detail_urls(self, group_ids: list) -> list:
        detail_url_template = f"{self.base_url}/sise/sise_group_detail.nhn?type=group&no={{}}"
        return [detail_url_template.format(group_id) for group_id in group_ids]

    def _fetch_group_stocks(self, detail_urls: list) -> list:
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

        tasks = [asyncio.ensure_future(self._fetch_group_stocks_async(url)) for url in detail_urls]
        group_stocks = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()

        return dict(group_stocks)

    async def _fetch_group_stocks_async(self, url: str) -> tuple:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await asyncio.sleep(0.1)    # Add delay to prevent server overload
                html = await response.text()
                group_name, stock_list = self._parse_group_stocks(html)

        return group_name, stock_list

    def _parse_group_stocks(self, html: str) -> tuple:
        start_tag, end_tag = 'style="padding-left:10px;">', '</td>'
        group_name = get_value_from_text(html, start_tag, end_tag)
        regex = '<a href="/item/main.naver\?code=(.*)">(.*)</a>'
        stock_list = re.findall(regex, html)

        return group_name, stock_list

    def fetch_stock_data(self) -> list:
        """Fetchs stock data for all KOSPI and KOSDAQ stock asynchronously."""
        self.group_stocks = self.fetch_stock_group()

        base_url = f'{self.base_url}/sise/sise_market_sum.nhn?sosok={{}}&page={{}}'
        urls = [base_url.format(sosok,page) for sosok in ['0','1'] for page in range(1,40)]

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

        tasks =[asyncio.ensure_future(self._fetch_stocks_async(url)) for url in urls]
        stock_pages = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()

        return stock_pages

    def fetch_stock_data_then_save(self):
        """Fetch stock data and save to the database in bulk."""
        try:
            fetched_stock_data = self.fetch_stock_data()
            for stock_data_list in fetched_stock_data:
                if not stock_data_list:
                    continue
                stock_objects = [StockKR(stock) for stock in stock_data_list]
                StockKR.objects.bulk_create(stock_objects)

        except Exception as e:
            print(f"Error occurred while saving stock data: {e}")

    async def _fetch_stocks_async(self, url: str) -> list:
        """Fetchs stocks from a specific URL asynchronously."""
        stocks = []
        sosok = get_value_from_text(url, 'sosok=', '&')
        exchange = 'KOSPI' if sosok == '0' else 'KOSDAQ'

        stock_detail_url = f'{self.base_url}/item/main.nhn?code={{}}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await asyncio.sleep(0.1)    # Add delay to prevent server overload
                html = await response.read()
                html = html.decode('euc-kr', 'ignore')

                stock_code_pattern ='<a href="/item/main.naver\?code=([a-zA-Z0-9]+).*>(.*)</a>'
                stock_codes = re.findall(stock_code_pattern, html)

                for code, name in stock_codes:
                    if not code:
                        continue
                    stock_details = await self._fetch_stock_detail(code, session, stock_detail_url.format(code))
                    stock = {
                        'country': 'kr',
                        'code': code,
                        'name': name,
                        'dname': disassemble_hangul(name),
                        'label': f'{code} {name}',
                        'exchange': exchange,
                        **stock_details
                    }
                    stocks.append(stock)
        return stocks

    async def _fetch_stock_detail(self, code: str, session: aiohttp.ClientSession, url: str) -> dict:
        """Fetchs detailed stock information."""
        async with session.get(url) as response:
            html = await response.read()
            html = html.decode('euc-kr', 'ignore')
            details = self._parse_stock_detail(html)
            return {
                'sector': details.get('sector', 'N/A'),
                'industry': details.get('industry', 'N/A'),
                'capital': details.get('capital', 0),
                'group_name': self._find_group_name(code),
                'avg_v50': 0    # Placeholder for furture candle data
            }

    def _parse_stock_detail(self, html: str) -> dict:
        """Parse HTML to extract stock details."""
        detail = {}
        detail['capital'] = self._extract_capital(html)
        detail['industry'] = self._extract_industry(html)
        detail['sector'] = detail['industry']   # Assuming sector is same as industry
        return detail

    def _extract_capital(self, html: str) -> int:
        """Extracts market capitalization.:"""
        start_tag, end_tag = '<em id="_market_sum">', '</em>'
        capital_str = get_value_from_text(html, start_tag, end_tag)

        clean_capital_str = re.sub(r'\s+', '', capital_str)  # '\s+'는 모든 공백, 탭, 줄바꿈을 제거
        if '조' in clean_capital_str:
            clean_capital_str = clean_capital_str.replace('조', '').zfill(4)
        return int(clean_capital_str.replace(',', '')) * 100000000

    def _extract_industry(self, html: str) -> str:
        """Extracts industry information."""
        match = re.search(r'업종명.*>(.*?)</a>', html)
        return match.group(1) if match else 'N/A'

    def _find_group_name(self, code: str) -> str:
        code = f'{code[:5]}0'
        for group_name, stock_list in self.group_stocks.items():
            for stock_code, stock_name in stock_list:
                if stock_code == code:
                    return group_name
        return 'N/A'

if __name__ == '__main__':
    from pymodm import connect
    connect('mongodb://localhost:27017/stockdb', alias='stockdb', connect=False)
    stock_fetcher_kr = StockFetcherKR()
    #print(stock_fetcher_kr.fetch_stock_group())
    #print(stock_fetcher_kr.fetch_stock_data())
    stock_fetcher_kr.fetch_stock_data_then_save()