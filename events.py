# events.py
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

# --- Global variables for event tracking ---
next_event_day = random.randint(2, 3)
last_event = None


def schedule_next_event(current_day):
    """Decide the next event day randomly (2–4 days ahead)."""
    global next_event_day
    next_event_day = current_day + random.randint(2, 4)


def trigger_event(market, day):
    """Trigger a random market event if it's the scheduled day."""
    global last_event, next_event_day

    if day != next_event_day:
        return None

    event = random.choice(EVENTS)
    name, imp, sec = event["name"], event["impact"], event["sector"]
    print(f"\nEVENT TRIGGERED: {name}! ({sec.upper()} sector, {imp:+.1%} impact)")

    for stock in market["stocks"]:
        if sec == "all" or stock["sector"] == sec:
            stock["price"] *= (1 + imp * random.uniform(0.8, 1.2))
            stock["price"] = round(stock["price"], 2)

    schedule_next_event(day)
    last_event = {"description": name, "impact": imp, "sector": sec, "active": True}
    return last_event
