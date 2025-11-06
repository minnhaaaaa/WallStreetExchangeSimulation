import random

# -----------------------------
# List of random market events
# -----------------------------
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


# -----------------------------
# EventManager Class Definition
# -----------------------------
class EventManager:
    def __init__(self):
        # Schedule first event randomly between days 2 and 3
        self.next_event_day = random.randint(2, 3)
        self.last_event = None

    def trigger_event(self, market, day):
        """Triggers a random market event every 2–4 days."""
        if day != self.next_event_day:
            return None  # No event today

        # Pick a random event
        event = random.choice(EVENTS)
        name, imp, sec = event["name"], event["impact"], event["sector"]
        print(f"\n⚠ EVENT TRIGGERED: {name}! ({sec.upper()} sector, {imp:+.1%} impact)")

        # Apply event impact to relevant stocks
        for symbol, stock in market["stocks"].items():
            if sec == "all" or stock["sector"] == sec:
                stock["price"] *= (1 + imp * random.uniform(0.8, 1.2))
                stock["price"] = round(stock["price"], 2)

        # Schedule next event in 2–4 days
        self.next_event_day = day + random.randint(2, 4)
        self.last_event = {
            "description": name,
            "impact": imp,
            "sector": sec,
            "active": True
        }

        return self.last_event


# ---------------------------------
# Optional standalone test
# ---------------------------------
if __name__ == "__main__":
    market = {
        "stocks": {
            "AAPL": {"sector": "tech", "price": 150},
            "XOM": {"sector": "energy", "price": 90},
            "JPM": {"sector": "banking", "price": 130},
            "PFE": {"sector": "health", "price": 40},
            "AMZN": {"sector": "retail", "price": 110},
        }
    }

    mgr = EventManager()
    print(f"Next event scheduled for Day {mgr.next_event_day}")

    for day in range(1, 9):
        print(f"\n📅 Day {day}")
        event = mgr.trigger_event(market, day)
        if event:
            print(f"Event: {event['description']} | Sector: {event['sector']} | Impact: {event['impact']:+.0%}")
        else:
            print("No major market event today.")

        for sym, info in market["stocks"].items():
            print(f"  {sym}: ${info['price']:.2f}")
