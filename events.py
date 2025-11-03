import random

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
        self.next_event_day = random.randint(2, 3)

    def trigger_event(self, market, day):
        if day != self.next_event_day:
            return  # no event today
        event = random.choice(EVENTS)
        name, imp, sec = event["name"], event["impact"], event["sector"]
        print(f"⚠ EVENT: {name}! {sec.upper()} sector {imp:+.1%}")

        for s, d in market["stocks"].items():
            if sec == "all" or d["sector"] == sec:
                d["price"] *= (1 + imp * random.uniform(0.8, 1.2))

        self.next_event_day += random.randint(2, 3)


