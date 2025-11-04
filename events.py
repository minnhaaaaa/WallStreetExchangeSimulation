import random
from typing import Dict, List, Tuple, Optional

# --- List of possible market events ---
EVENTS = [
    {"name": "Black Monday Crash", "impact": -0.30, "sector": "all"},
    {"name": "Tech Boom", "impact": +0.15, "sector": "tech"},
    {"name": "Oil Scandal", "impact": -0.12, "sector": "energy"},
    {"name": "Pharma Breakthrough", "impact": +0.20, "sector": "healthcare"},
    {"name": "Insider Scandal", "impact": -0.50, "sector": "single_stock"},
    {"name": "Takeover Bid", "impact": +0.40, "sector": "single_stock"},
    {"name": "Inflation Worries", "impact": -0.07, "sector": "all"},
]

# --- Handles when and which event occurs ---
class EventManager:
    def __init__(self, events: Optional[List[Dict]] = None):
        self.events = events or EVENTS
        self.next_event_day = random.randint(1, 3)

    def schedule_next(self, day: int):  # Pick next event day randomly
        self.next_event_day = day + random.randint(2, 3)

    def pick(self):  # Choose random event
        return random.choice(self.events)

# --- Apply market impact ---
def trigger_event(market: Dict, day: int, manager: Optional[EventManager] = None):
    manager = manager or EventManager()
    if day < manager.next_event_day:
        return None

    event = manager.pick()
    name, impact, sector = event["name"], event["impact"], event["sector"]
    stocks = market["stocks"]
    impacted = []

    # Helper to update prices
    def update(symbols):
        for s in symbols:
            st = stocks[s]
            old = st["price"]
            st["price"] = round(max(0.01, old * (1 + impact * (1 + random.uniform(-0.02, 0.02)))), 2)
            impacted.append((s, (st["price"] - old) / old))

    # Apply based on sector type
    if sector == "all":
        update(stocks.keys())
        print(f"⚠️ {name}! All stocks change by {impact:+.1%}")
    elif sector == "single_stock":
        sym = random.choice(list(stocks))
        update([sym])
        print(f"⚠️ {name}! {sym} {'jumps' if impact > 0 else 'drops'} {impact:+.1%}")
    else:
        sector_stocks = [s for s, v in stocks.items() if v["sector"] == sector]
        update(sector_stocks or random.sample(list(stocks), k=3))
        print(f"⚠️ {name}! {sector.capitalize()} sector {impact:+.1%}")

    # Display top affected stocks
    for s, pct in sorted(impacted, key=lambda x: abs(x[1]), reverse=True)[:3]:
        print(f"  - {s}: {pct:+.2%} → {stocks[s]['price']}")

    manager.schedule_next(day)
    return {"event": event, "impacted": impacted}

# --- Example test run ---
if __name__ == "__main__":
    market = {
        "stocks": {
            "AAPL": {"price": 150, "sector": "tech"},
            "XOM": {"price": 100, "sector": "energy"},
            "PFE": {"price": 40, "sector": "healthcare"},
            "TSLA": {"price": 250, "sector": "auto"},
        }
    }
    mgr = EventManager()
    for d in range(1, 8):
        print(f"\nDay {d}")
        res = trigger_event(market, d, mgr)
        if not res:
            print("No major event today.")
