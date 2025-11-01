class Stock:
    def __init__(self, symbol, name, sector, price, volatility):
        self.symbol = symbol
        self.name = name
        self.sector = sector
        self.price = price
        self.volatility = volatility
        self.history = [price]

class Market:
    def __init__(self, data_path="market/stocks.json"):
        self.data_path = data_path
        self.stocks = {}
        self.day = 1
        self.market_sentiment = "neutral"
        self.load_stocks()

    def load_stocks(self):
        data = load_json(self.data_path)
        for item in data:
            stock = Stock(
                item["symbol"],
                item["name"],
                item["sector"],
                item["price"],
                item["volatility"]
            )
            self.stocks[stock.symbol] = stock
