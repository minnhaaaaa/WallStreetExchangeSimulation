import random
def generate_tip(stocks):
    if random.random()>0.50:
        return None
    stock = random.choice(stocks)
    name = stock["name"]
    direction = random.choice(["up", "down"])
    is_true = random.choice([True, False])
    tips_positive = [
        f"Word is out that {name} is about to announce record profits!",
        f"Rumor: {name} may merge with a top tech company.",
        f"Sources say {name} just secured a massive government contract."
        f"Early reports suggest {name} will exceed quarterly expectations."
        f"{name}set to enter new market with strong growth potential."
        f"Investor sentiment for{name} is at an all-time high."
        f"Insiders cliam {name} is in talks for international expansion."
        f"{name} is rumored to announce a breakthrough product next quarter."
        f"Speculation mounts that{name} will issue a dividend increase."
        f"{name}'s CEO scheduled for a major keynote at an  industry conference
    ]

    tips_negative = [
        f"Leaked memo: {name} might be under investigation.",
        f"Analysts suspect {name} is overvalued — expect a dip.",
        f"Rumor says {name} is facing internal layoffs soon."
        f"Whistleblower alleges accounting irregularities at {name}."
        f"supply chain disruptions may impact {name}'s earnings."
        f"{name} faces stiff competition in a shrinking market."
        f"Pending lawsuit could affect {name}'s leadership."
        f"Unconfirmed reports of customer data breach at (name}."
        f"Global market instability may hit{name}'s overseas revenue."
        f"Pending lawsuit could affect {name}'s financial stability."
        
    ]
    if direction == "up":
        message = random.choice(tips_positive)
    else:
        message = random.choice(tips_negative)

    impact_strength = random.uniform (0.02,0.10)

    return {
        "stock": stock["name"],
        "direction":direction,
        "truth":is_true,
        "impact":impact_strength,
        "message": message,
    }

def apply_tip_outcome(stocks, tip):
    stock_name = tip["stock"]
    impact = tip["impact"]
    direction = tip["direction"]
    truth = tip["truth"]

    for stock in stocks:
        if stock["name"] == stock_name:
            if truth:
                if direction=="up":
                    stock["price"] = round(stock["price"] * (1 + impact),2)
                    print(f"✅ The tip about {stock_name} was TRUE! Prices surged by {impact*100:.1f}%")
                else: 
                    stock["price"] = round(stock["price"] * (1 - impact), 2)
                    print(f"⚠️ The tip about {stock_name} was TRUE! Prices dropped by {impact*100:.1f}%")
            else:
                if direction == "up":
                    stock["price"] = round(stock["price"] * (1 - impact),2)
                    print(f"❌ The tip about {stock_name} was FALSE! Prices fell by {impact*100:.1f}% instead")
                else: 
                    stock["price"] = round(stock["price"] * (1 + impact), 2)
                    print(f"❌ The tip about {stock_name} was FALSE! Prices rose by {impact*100:.1f}% instead")
            break


