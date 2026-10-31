import requests
from langchain.tools import tool


# A stock price
@tool(
    name_or_callable="get_stock_price",
    description="Get the latest stock price for a stock symbol.",
)
def get_stock_price(symbol: str):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }  # Yahoo blocks requests that don't say which browser they are
    data = requests.get(url, headers=headers, timeout=10).json()
    meta = data["chart"]["result"][0]["meta"]
    return {
        "symbol": symbol,
        "price": meta["regularMarketPrice"],
        "currency": meta["currency"],
    }
