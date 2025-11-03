import json,os,random
from news import generate_daily_news
from tips import generate_tip,apply_tip_outcome
from events import generate_market_event

class Market:
    def __init__(self, data_path="data/stocks.json"):
        with open(data_path,"r") as f:
            self.stocks = json.load(f)
        self.day = 1
        self.sentiment = "neutral"
        self.event = None
        self.history = []
        self.active_tips = []

    def update_price(self):
        sentiment_effect = {"positive":1.05,"negative":0.95,"neutral":1.00}
        daily_multiplier = sentiment_effect[self.sentiment]
        event_multiplier = self.event["impact"] if self.event else 1.0
        total_effect = daily_multiplier*event_multiplier
        for stock in self.stocks:
            change = random.uniform(0.95,1.05)
            stock["price"] = round(stock["price"]*total_effect*change,2)
    
    def next_day(self):
        self.day+=1
        news,sentiment = generate_daily_news()
        self.sentiment = sentiment

        for tip in self.active_tips[:]:
            if self.day - tip["day"] >= 1:
                self.apply_tip_outcome(self.stocks,tip["tip"])
                self.active_tips.remove(tip)
        tip = generate_tip(self.stocks)
        if tip:
            self.active_tips.append({"tip":tip,"day":self.day})
        
        self.event = generate_market_event()
        self.update_price()

        self.history.append({
            "day":self.day,
            "sentiment":self.sentiment,
            "event":self.event["description"] if self.event else None,
            "tip":tip,
            "news":news,
            "stocks":{s["name"]: s["price"] for s in self.stocks}
        })

        return {
            "day": self.day,
            "news": news,
            "sentiment": self.sentiment,
            "tip": tip,
            "event": self.event["description"] if self.event else None,
            "stocks": {s["name"]: s["price"] for s in self.stocks}
        }
