import yfinance as yf


class Stock(dict):
    def __init__(self, symbol: str = "MSFT", shares=0, average=0):
        self.symbol = symbol
        self.shares = shares
        self.average = average

    def get_data(self):
        return {'symbol': self.symbol, 'shares': self.shares, 'average': self.average}


class StockUtils():

    def get(symbol: str) -> float:
        stock = yf.Ticker(symbol)
        stock_price = stock.info['regularMarketPrice']
        return stock_price

    def convert(price: float) -> int:

        result = round(price)
        result = int(result)
        return result
