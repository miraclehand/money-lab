import requests
from app.fetchers.stock_fetcher import StockFetcher


class USStockFetcher(StockFetcher):
    def fetch_stock_data(self, ticker: str):
        api_key = "your_alpha_vantage_api_key"
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if "Time Series (Daily)" in data:
                latest_data = list(data["Time Series (Daily)"].values())[0]
                stock_data = {
                    'ticker': ticker,
                    'name': "Apple Inc.",
                    'price': float(latest_data["4. close"])
                }
                return stock_data
            else:
                raise Exception(f"Error in fetching data for {ticker}: {data}")
        else:
            raise Exception(f"Failed to fetch data for {ticker}")

    def fetch_and_upsert_stock_data(self, ticker: str):
        pass
