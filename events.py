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
        self.last_event = None

    def trigger_event(self, market, day):
        if day != self.next_event_day:
            return  None# no event today
        event = random.choice(EVENTS)
        name, imp, sec = event["name"], event["impact"], event["sector"]
        print(f"\n⚠ EVENT {name} TRIGGERED! {sec.upper()} sector, {imp:+.1%} impact")

        affected_stocks = []
        for s in market.stocks:
            if sec == "all" or s["sector"] == sec:
                variation = random.uniform(0.8, 1.2)
                s["price"] = round(s["price"] * (1 + imp * variation), 2)
                affected_stocks.append(s["name"])

        self.next_event_day += random.randint(2, 3)
        self.last_event = {"name": name, "impact": imp, "sector": sec, "affected": affected_stocks}
        return self.last_event

