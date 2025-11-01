def get_insider_tip(market):
    stock = random.choice(list(market.stocks.keys()))
    reliability = random.uniform(0.5, 0.9) 

    tips_positive = [
        f"Word is out that {stock} is about to announce record profits!",
        f"Rumor: {stock} may merge with a top tech company.",
        f"Sources say {stock} just secured a massive government contract."
    ]

    tips_negative = [
        f"Leaked memo: {stock} might be under investigation.",
        f"Analysts suspect {stock} is overvalued — expect a dip.",
        f"Rumor says {stock} is facing internal layoffs soon."
    ]

    is_positive = random.choice([True, False])
    message = random.choice(tips_positive if is_positive else tips_negative)

    impact = "up" if is_positive else "down"

    return {
        "stock_symbol": stock,
        "message": message,
        "reliability": reliability,
        "impact": impact
    }

def apply_tip_outcome(market, tip):
    if random.random() <= tip["reliability"]:
        if tip["impact"] == "up":
            market.stocks[tip["stock_symbol"]].price *= random.uniform(1.05, 1.20)
        else:
            market.stocks[tip["stock_symbol"]].price *= random.uniform(0.8, 0.95)
        return f"The tip about {tip['stock_symbol']} turned out TRUE!"
    else:
        if tip["impact"] == "up":
            market.stocks[tip["stock_symbol"]].price *= random.uniform(0.8, 0.95)
        else:
            market.stocks[tip["stock_symbol"]].price *= random.uniform(1.05, 1.20)
        return f"The tip about {tip['stock_symbol']} was FAKE!"
