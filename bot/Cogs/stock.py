import yfinance as yf


class Stock():
    def __init__(self, symbol: str = "MSFT"):
        self.symbol = symbol


class StockUtils():

    def get(symbol: str) -> float:
        stock = yf.Ticker(symbol)
        stock_price = stock.info['regularMarketPrice']
        return stock_price

    def convert(price: float)
