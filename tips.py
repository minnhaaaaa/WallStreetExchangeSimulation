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
        f"Sources say {name} just secured a massive government contract.",
        f"Early reports suggest {name} will exceed quarterly expectations.",
        f"{name} set to enter new market with strong growth potential.",
        f"Investor sentiment for {name} is at an all-time high.",
        f"Insiders claim {name} is in talks for international expansion.",
        f"{name} is rumored to announce a breakthrough product next quarter.",
        f"Speculation mounts that {name} will issue a dividend increase.",
        f"{name}'s CEO scheduled for a major keynote at an industry conference",
    ]

    tips_negative = [
        f"Leaked memo: {name} might be under investigation.",
        f"Analysts suspect {name} is overvalued — expect a dip.",
        f"Rumor says {name} is facing internal layoffs soon.",
        f"Whistleblower alleges accounting irregularities at {name}.",
        f"supply chain disruptions may impact {name}'s earnings.",
        f"{name} faces stiff competition in a shrinking market.",
        f"Pending lawsuit could affect {name}'s leadership.",
        f"Unconfirmed reports of customer data breach at {name}.",
        f"Global market instability may hit {name}'s overseas revenue.",
        f"Pending lawsuit could affect {name}'s financial stability.",   
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

def apply_tip_outcome(tip):
    stock_name = tip["stock"]
    impact = tip["impact"]
    direction = tip["direction"]
    truth = tip["truth"]

    price_multiplier = 1.0
    if truth:
        final_sign = 1 if direction == "up" else -1
        outcome_msg = f"✅ The tip about {stock_name} was TRUE! Prices moved {direction} by {impact*100:.1f}%"
        
    else:
        final_sign = -1 if direction == "up" else 1
        outcome_msg = f"❌ The tip about {stock_name} was FALSE! Prices moved in the opposite direction by {impact*100:.1f}%"

    price_multiplier = 1 + (impact * final_sign)
    print(outcome_msg)    
    return stock_name, price_multiplier
    

