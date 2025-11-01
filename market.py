class Stock:
    def __init__(self, name, symbol, price, volatility):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.volatility = volatility  

class Market:
    def __init__(self):
        self.stocks = {
            "AAPL": Stock("Apple Inc.", "AAPL","Technology", 120.0, 0.03),
            "XOM": Stock("Exxon Mobil", "XOM","Energy", 55.0, 0.04),
        }

