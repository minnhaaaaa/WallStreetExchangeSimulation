import random
import math
from typing import Dict, List, Tuple, Optional

EVENTS = [
    {"name": "Black Monday Crash", "impact": -0.30, "sector": "all"},
    {"name": "Tech Boom", "impact": +0.15, "sector": "tech"},
    {"name": "Oil Scandal", "impact": -0.12, "sector": "energy"},
    {"name": "Banking Confidence Surge", "impact": +0.10, "sector": "banking"},
    {"name": "Pharma Breakthrough", "impact": +0.20, "sector": "healthcare"},
    {"name": "Regulatory Headache", "impact": -0.10, "sector": "tech"},
    {"name": "Interest Rate Cut", "impact": +0.08, "sector": "all"},
    {"name": "Inflation Worries", "impact": -0.07, "sector": "all"},
    {"name": "Commodity Spike", "impact": +0.12, "sector": "materials"},
    {"name": "Energy Supply Shock", "impact": +0.18, "sector": "energy"},
    {"name": "Insider Scandal", "impact": -0.50, "sector": "single_stock"},
    {"name": "Takeover Bid", "impact": +0.40, "sector": "single_stock"},
    {"name": "Crypto FOMO", "impact": +0.25, "sector": "crypto"},
    {"name": "Supply Chain Cleared", "impact": +0.09, "sector": "industrial"},
    {"name": "Earnings Miss", "impact": -0.18, "sector": "consumer"}
]

EVENT_TEMPLATES = {
    "all": "⚠️ MARKET EVENT: {name}! All stocks change by {pct:+.1%}!",
    "sector": "⚠️ MARKET EVENT: {name}! {sector_cap} sector changes by {pct:+.1%}!",
    "single_stock_up": "⚠️ MARKET EVENT: {name}! {symbol} ({company}) jumps {pct:+.1%}!",
    "single_stock_down": "⚠️ MARKET EVENT: {name}! {symbol} ({company}) plunges {pct:+.1%}!",
}

class EventManager:
    def __init__(self, events_list: Optional[List[Dict]] = None):
        self.events = events_list if events_list is not None else EVENTS
        self.next_event_day = random.choice([1, 2, 3])
        self.last_event = None

    def schedule_next(self, current_day: int):
        gap = random.choice([2, 3])
        self.next_event_day = current_day + gap

    def pick_event(self) -> Dict:
        return random.choice(self.events)

_default_manager = EventManager()

def _detect_stocks_dict(market: Dict) -> Dict:
    if not isinstance(market, dict):
        raise ValueError("market must be a dict")
    if "stocks" in market and isinstance(market["stocks"], dict):
        return market["stocks"]
    for k in ("symbols", "prices", "market"):
        if k in market and isinstance(market[k], dict):
            return market[k]
    raise ValueError("Could not find 'stocks' dict in market. Expected market['stocks'] = {symbol: {...}}")

def _apply_impact_to_stock(stock_info: Dict, impact: float, gentle_noise: float = 0.02) -> float:
    if "price" not in stock_info:
        return 0.0
    base_price = float(stock_info["price"])
    noise = random.uniform(-gentle_noise, gentle_noise)
    final_multiplier = 1.0 + impact * (1.0 + noise)
    new_price = max(0.01, base_price * final_multiplier)
    stock_info["price"] = round(new_price, 4)
    pct_change = (stock_info["price"] - base_price) / base_price
    return pct_change

def _apply_event_to_market(market: Dict, event: Dict) -> List[Tuple[str, float]]:
    stocks = _detect_stocks_dict(market)
    impacted = []
    ev_sector = event.get("sector", "all")
    impact = event.get("impact", 0.0)
    def apply_to_symbols(symbols: List[str]):
        for s in symbols:
            info = stocks.get(s)
            if not info:
                continue
            pct = _apply_impact_to_stock(info, impact)
            impacted.append((s, pct))
    if ev_sector == "all":
        apply_to_symbols(list(stocks.keys()))
    elif ev_sector == "single_stock":
        candidates = list(stocks.keys())
        if not candidates:
            return impacted
        chosen = random.choice(candidates)
        apply_to_symbols([chosen])
    else:
        matched = [sym for sym, info in stocks.items() if info.get("sector", "").lower() == ev_sector.lower()]
        if not matched:
            fallback = random.sample(list(stocks.keys()), k=min(3, len(stocks)))
            apply_to_symbols(fallback)
        else:
            apply_to_symbols(matched)
    return impacted

def trigger_event(market: Dict, day: int, manager: Optional[EventManager] = None) -> Optional[Dict]:
    if manager is None:
        manager = _default_manager
    if day < manager.next_event_day:
        return None
    event = manager.pick_event()
    impacted = _apply_event_to_market(market, event)
    name = event.get("name", "Market Event")
    impact = event.get("impact", 0.0)
    sector = event.get("sector", "all")
    if sector == "all":
        print(EVENT_TEMPLATES["all"].format(name=name, pct=impact))
    elif sector == "single_stock":
        if impacted:
            sym, pct = impacted[0]
            info = _detect_stocks_dict(market).get(sym, {})
            company = info.get("name", "Unknown")
            key = "single_stock_up" if impact > 0 else "single_stock_down"
            print(EVENT_TEMPLATES[key].format(name=name, symbol=sym, company=company, pct=pct))
        else:
            print(f"⚠️ MARKET EVENT: {name}! But no stocks were impacted.")
    else:
        sector_cap = sector.capitalize()
        print(EVENT_TEMPLATES["sector"].format(name=name, sector_cap=sector_cap, pct=impact))
    if impacted:
        impacted_sorted = sorted(impacted, key=lambda x: abs(x[1]), reverse=True)
        print("→ Affected stocks:")
        top = impacted_sorted[:5]
        stocks_dict = _detect_stocks_dict(market)
        for sym, pct in top:
            info = stocks_dict.get(sym, {})
            company = info.get("name", "")
            print(f"   - {sym} {('('+company+')') if company else ''}: {pct:+.2%} (new {info.get('price')})")
    else:
        print("→ No stocks were changed by this event.")
    manager.last_event = {"day": day, "event": event}
    manager.schedule_next(day)
    return {"day": day, "event": event, "impacted": impacted}

if __name__ == "__main__":
    sample_market = {
        "day": 1,
        "stocks": {
            "AAPL": {"name": "Apple Inc.", "sector": "tech", "price": 150.0, "volatility": 0.02},
            "MSFT": {"name": "Microsoft Corp.", "sector": "tech", "price": 310.0, "volatility": 0.02},
            "XOM": {"name": "Exxon Mobil", "sector": "energy", "price": 92.5, "volatility": 0.03},
            "JPM": {"name": "JPMorgan Chase", "sector": "banking", "price": 131.0, "volatility": 0.03},
            "PFE": {"name": "Pfizer", "sector": "healthcare", "price": 40.0, "volatility": 0.04},
            "BHP": {"name": "BHP Group", "sector": "materials", "price": 50.0, "volatility": 0.03},
            "TSLA": {"name": "Tesla", "sector": "auto", "price": 240.0, "volatility": 0.06},
            "GME": {"name": "GameStop", "sector": "consumer", "price": 12.0, "volatility": 0.10},
            "BTC-USD": {"name": "Bitcoin (ETF proxy)", "sector": "crypto", "price": 30000.0, "volatility": 0.08},
        }
    }
    mgr = EventManager()
    print(f"First scheduled event day: {mgr.next_event_day}")
    for d in range(1, 11):
        print("\n" + "="*40)
        print(f"Day {d}")
        res = trigger_event(sample_market, d, manager=mgr)
        if res is None:
            print("No market event today.")
        for s, info in sample_market["stocks"].items():
            daily = random.uniform(-0.03, 0.03)
            info["price"] = round(max(0.01, info["price"] * (1 + daily)), 4)
        print("Sample prices:")
        for sym in list(sample_market["stocks"].keys())[:5]:
            print(f"  {sym}: {sample_market['stocks'][sym]['price']}")
