import requests
from .stock_fetcher import StockFetcher

class StockFetcherUS(StockFetcher):
    def fetch_stock_data(self, stock_code: str):
        api_key = "your_alpha_vantage_api_key"
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_code}&apikey={api_key}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if "Time Series (Daily)" in data:
                latest_data = list(data["Time Series (Daily)"].values())[0]
                stock_data = {
                    'code': stock_code,
                    'name': "Apple Inc.",
                    'price': float(latest_data["4. close"])
                }
                return stock_data
            else:
                raise Exception(f"Error in fetching data for {stock_code}: {data}")
        else:
            raise Exception(f"Failed to fetch data for {stock_code}")

