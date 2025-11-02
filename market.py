import json,os,random

class Stock:
    def __init__(self, symbol, name, sector, price, volatility):
        self.symbol = symbol
        self.name = name
        self.sector = sector
        self.price = price
        self.volatility = volatility
        self.history = [price]

    def update_price(self,event_factor = 1.0,sentiment_factor = 1.0):
        change_percent = random.uniform(-self.volatility,self.volatility)
        self.price*= (1+(change_percent*event_factor*sentiment_factor))
        self.price = round(self.price,2)
        self.history.append(self.price)

class Market:
    def __init__(self, data_path="data/stocks.json"):
        self.stocks = []
        self.day = 1
        self.market_sentiment = "neutral"
        self.sentiment_factor = 1.0
        self.load_stocks(data_path)

    def load_stocks(self,data_path):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Stock data not found at {data_path}")
        with open (data_path,"r") as df:
            stock_data = json.load(df)
        for item in stock_data:
            stock = Stock(item["symbol"],item["name"],item["sector"],item["price"],item["volatility"])
            self.stocks.append(stock)
        print(f"Loaded {len(self.stocks)} stocks from {data_path}")
