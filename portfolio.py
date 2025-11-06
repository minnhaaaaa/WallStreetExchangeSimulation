import json

class Portfolio:
    def __init__(self, starting_balance=100000):
        self.balance = starting_balance
        self.holdings = {}  # stock_name → {"quantity": int, "avg_price": float}
        self.history = []   # track daily snapshots

    def buy_stock(self, stock_name, price, quantity):
        total_cost = price * quantity
        if total_cost > self.balance:
            print(f"❌ Not enough balance to buy {quantity} shares of {stock_name}.")
            return False
        
        # update holdings
        if stock_name not in self.holdings:
            self.holdings[stock_name] = {"quantity": 0, "avg_price": 0.0}

        prev_qty = self.holdings[stock_name]["quantity"]
        prev_avg = self.holdings[stock_name]["avg_price"]

        # compute new average price
        new_qty = prev_qty + quantity
        new_avg = ((prev_qty * prev_avg) + total_cost) / new_qty

        self.holdings[stock_name]["quantity"] = new_qty
        self.holdings[stock_name]["avg_price"] = round(new_avg, 2)

        self.balance -= total_cost
        print(f"✅ Bought {quantity} shares of {stock_name} at ₹{price:.2f} each.")
        return True

    def sell_stock(self, stock_name, price, quantity):
        if stock_name not in self.holdings or self.holdings[stock_name]["quantity"] < quantity:
            print(f"❌ You don’t own enough {stock_name} shares to sell.")
            return False

        total_sale = price * quantity
        self.holdings[stock_name]["quantity"] -= quantity
        self.balance += total_sale

        print(f"💰 Sold {quantity} shares of {stock_name} at ₹{price:.2f} each.")

        if self.holdings[stock_name]["quantity"] == 0:
            del self.holdings[stock_name]

        return True

    def get_portfolio_value(self, market_stocks):
        total = self.balance
        for s in market_stocks:
            name = s["name"]
            price = s["price"]
            if name in self.holdings:
                total += self.holdings[name]["quantity"] * price
        return round(total, 2)

    def summary(self, market_stocks):
        print("\n📊 Portfolio Summary:")
        print(f"Available Cash: ₹{self.balance:,.2f}")
        for s in market_stocks:
            name = s["name"]
            price = s["price"]
            if name in self.holdings:
                qty = self.holdings[name]["quantity"]
                avg = self.holdings[name]["avg_price"]
                curr_val = qty * price
                print(f" - {name}: {qty} shares | Avg ₹{avg:.2f} | Current ₹{price:.2f} | Value ₹{curr_val:.2f}")
        total_value = self.get_portfolio_value(market_stocks)
        print(f"💼 Total Portfolio Value: ₹{total_value:,.2f}\n")

