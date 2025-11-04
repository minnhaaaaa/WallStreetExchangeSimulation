import random

# List of market events with impact% and affected sector
EVENTS = [
    {"name": "Black Monday Crash", "impact": -0.2, "sector": "all"},
    {"name": "Tech Boom", "impact": +0.15, "sector": "tech"},
    {"name": "Oil Scandal", "impact": -0.1, "sector": "energy"},
    {"name": "Bank Crisis", "impact": -0.12, "sector": "banking"},
    {"name": "Green Energy Surge", "impact": +0.18, "sector": "energy"},
    {"name": "Pharma Breakthrough", "impact": +0.22, "sector": "health"},
    {"name": "Cyber Attack", "impact": -0.15, "sector": "tech"},
    {"name": "AI Revolution", "impact": +0.25, "sector": "tech"},
    {"name": "Real Estate Slump", "impact": -0.1, "sector": "real_estate"},
    {"name": "Consumer Boom", "impact": +0.1, "sector": "retail"},
    {"name": "Trade War", "impact": -0.08, "sector": "industrial"},
    {"name": "Crypto Crash", "impact": -0.2, "sector": "finance"},
    {"name": "Interest Rate Cut", "impact": +0.05, "sector": "all"},
    {"name": "Regulatory Crackdown", "impact": -0.1, "sector": "finance"},
    {"name": "M&A Frenzy", "impact": +0.12, "sector": "all"},
]

class EventManager:
    def __init__(self):
        # First event will happen randomly on day 2 or 3
        self.next_event_day = random.randint(2, 3)

    def trigger_event(self, market, day):
        # Only trigger event on the scheduled day
        if day != self.next_event_day:
            return  

        # Choose a random market event
        event = random.choice(EVENTS)
        name, imp, sec = event["name"], event["impact"], event["sector"]

        # Display event information
        print(f"⚠ EVENT: {name}! {sec.upper()} sector {imp:+.1%}")

        # Apply price change to affected stocks
        for symbol, stock in market["stocks"].items():
            # If event affects all or specific stock's sector
            if sec == "all" or stock["sector"] == sec:
                # Apply impact with slight randomness for realism
                stock["price"] *= (1 + imp * random.uniform(0.8, 1.2))

        # Schedule next event in 2–3 days
        self.next_event_day += random.randint(2, 3)


# -------------------------------------
# Standalone run test (only when run directly)
# -------------------------------------
if __name__ == "__main__":
    # Sample market for testing
    market = {
        "stocks": {
            "AAPL": {"price": 150, "sector": "tech"},
            "XOM": {"price": 100, "sector": "energy"},
            "JPM": {"price": 90, "sector": "banking"},
            "PFE": {"price": 40, "sector": "health"},
        }
    }
    
    mgr = EventManager()
    print(f"Next event scheduled on day: {mgr.next_event_day}")

    # Simulate 7 days
    for day in range(1, 8):
        print(f"\nDay {day}")
        mgr.trigger_event(market, day)

        # Print updated stock prices
        for sym, data in market["stocks"].items():
            print(f"  {sym}: {data['price']:.2f}")
