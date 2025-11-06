import json,random
from news import generate_daily_news
from tips import generate_tip,apply_tip_outcome
from events import EventManager
from portfolio import Portfolio

class Market:
    def __init__(self, data_path="data/stocks.json"):
        with open(data_path,"r") as f:
            self.stocks = json.load(f)
        self.day = 0
        self.sentiment = "neutral"
        self.event = None
        self.history = []
        self.active_tips = []
        self.event_manager = EventManager()
        self.portfolio = Portfolio()

    def update_price(self,sentiment_multiplier, news_sector, news_impact, tip_multipliers):
        event_general_multiplier = 1.0
        event_impact_value = 0.0
        event_sector = None

        if self.event and self.event.get("active", False):
            event_impact_value = self.event["impact"]
            event_sector = self.event["sector"]
            if event_sector == "all":
                event_general_multiplier = 1.0 + event_impact_value
                event_sector = None

        for stock in self.stocks:
            stock_name = stock["name"]

            #1.Random change
            random_change = random.uniform(0.95, 1.05) 
            # 2. General Market Sentiment (from news)
            
            # 3. Sector-Specific News Impact
            sector_news_multiplier = 1.0
            if news_sector and stock["sector"].lower() == news_sector.lower():
                effect_sign = 1 if self.sentiment == "positive" else -1
                sector_news_multiplier = 1.0 + (effect_sign * abs(news_impact) * 0.5)

            # 4. Sector-Specific Event Impact
            sector_event_multiplier = 1.0
            if event_sector and stock["sector"].lower() == event_sector.lower():
                variation = random.uniform(0.8, 1.2)
                sector_event_multiplier = 1 + (event_impact_value * variation)
                
            # 5. Tip Impact
            tip_multiplier = tip_multipliers.get(stock_name, 1.0) # Apply 1.0 if no tip

            # 6. Total Daily Price Effect
            total_effect = (
                random_change * sentiment_multiplier * event_general_multiplier * sector_news_multiplier * sector_event_multiplier * tip_multiplier
            )

            stock["price"] = round(stock["price"] * total_effect, 2)
            stock["price"] = max(0.01, stock["price"])
    
    def next_day(self):
        self.day+=1

        #Step 1: Generate daily news
        headline,sentiment,sector,impact = generate_daily_news()
        self.sentiment = sentiment
        print(f"\n======================================")
        print(f"💰 MARKET OPENING: DAY {self.day}")
        print(f"======================================")
        print(f"📰 News: {headline} ({sentiment.upper()}, sector={sector}, impact={impact:+.1%})")

        #Apply news
        sentiment_effect = {"positive": 1 + abs(impact), "negative": 1 - abs(impact), "neutral": 1.0}
        sentiment_multiplier = sentiment_effect[self.sentiment]
        news_data = {"headline": headline, "sentiment": sentiment, "sector": sector, "impact": impact}
        
        #Step 2: Apply tips ( 1 day delay )
        tip_multipliers={}
        for i in self.active_tips[:]:       #format for self.active_tips is [ { "tip": tip, "day": 1 }, { "tip": tip2, "day": 2 } ]
            if self.day - i["day"] >= 1:
                stock_name,multiplier = apply_tip_outcome(i["tip"])
                tip_multipliers[stock_name] = multiplier
                self.active_tips.remove(i)
            if not tip_multipliers:
                print("No tips matured today...")

        #Generate tip possibly
        tip = generate_tip(self.stocks)
        if tip:
            self.active_tips.append({"tip":tip,"day":self.day})
        
        #Step 3: Generate event possibly

        new_event = self.event_manager.trigger_event(self, self.day)
        if new_event:
            self.event = new_event
        elif self.event and self.event.get("active", False) == False:
            self.event = None

        previous_prices = {s["name"]: s["price"] for s in self.stocks}
        
        self.update_price(sentiment_multiplier, sector, impact, tip_multipliers) 
        current_prices = {s["name"]: s["price"] for s in self.stocks}

        self.history.append({
            "day": self.day,
            "sentiment": self.sentiment,
            "event": self.event["description"] if self.event else None,
            "tip": tip["message"] if tip else None, # Storing the tip message
            "news": news_data,
            # Store prices along with the previous day's closing price
            "stocks": [{
                "name": s["name"],
                "price": s["price"],
                "prev_price": previous_prices[s["name"]]
            } for s in self.stocks]
        })


        return {
            "day": self.day,
            "news": news_data,
            "sentiment": self.sentiment,
            "tip": tip["message"] if tip else None,
            "event": self.event["description"] if self.event else None,
            "stocks": current_prices
        }
    def get_stocks(self):
        return self.stocks

    def get_history(self):
        return self.history[-1] if self.history else None
    
    def get_active_tips(self):
        return self.active_tips
