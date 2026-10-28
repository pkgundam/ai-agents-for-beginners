import requests


# A stock price
def get_stock_price(symbol: str):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Yahoo blocks requests that don't say which browser they are
    data = requests.get(url, headers=headers, timeout=10).json()
    meta = data["chart"]["result"][0]["meta"]
    return {
        "symbol": symbol,
        "price": meta["regularMarketPrice"],
        "currency": meta["currency"],
    }


# What the LLM sees: a name, a description and the inputs
STOCK_TOOL = {
    "type": "function",
    "name": "get_stock_price",
    "description": "Get the latest stock price for a stock symbol.",
    "parameters": {
        "type": "object",
        "properties": {
            "symbol": {"type": "string", "description": "The stock symbol, for example TSLA for Tesla"},
        },
        "required": ["symbol"],
    },
}

if __name__ == "__main__":
    symbol = "AAPL"
    print(f"Getting the stock price for {symbol}...")
    stock_price = get_stock_price(symbol)
    print(stock_price)