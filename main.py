# main.py
import sys
import random
from market import Market
from events import trigger_event  

def display_stocks(market):
    print("\n📈 Current Stock Prices:")
    last_day_data = market.get_history()
    
    print(f"{'Name':<15}{'Sector':<10}{'Price (₹)':<15}{'Change':<10}{'Owned':<10}")
    print("-------------------------------------------------------------")
    
    for stock in market.get_stocks():
        name = stock["name"]
        price = stock["price"]
        sector = stock["sector"]
        
        prev_price = None
        if last_day_data:
            for s_hist in last_day_data["stocks"]:
                if s_hist["name"] == name:
                    prev_price = s_hist["prev_price"]
                    break

        change_str = "-"
        if prev_price and prev_price > 0:
            change_pct = (price - prev_price) / prev_price
            change_str = f"{change_pct:+.1%}"
        
        qty = market.portfolio.holdings.get(name, {}).get("quantity", 0)
        print(f"{name:<15}{sector:<10}{price:<15.2f}{change_str:<10}{qty:<10}")


def trade_menu(market):
    while True:
        market.portfolio.summary(market.get_stocks())
        action = input("Trade (buy/sell) or Back: ").lower().strip()
        
        if action == 'back':
            break
        if action not in ('buy', 'sell'):
            print("Invalid action. Please enter 'buy', 'sell', or 'back'.")
            continue

        stock_name = input(f"Enter stock name to {action}: ").strip()
        selected_stock = next((s for s in market.get_stocks() if s["name"].lower() == stock_name.lower()), None)
        if not selected_stock:
            print("Stock not found.")
            continue

        try:
            quantity = int(input(f"Enter quantity: "))
            if quantity <= 0:
                raise ValueError
        except ValueError:
            print("Invalid quantity.")
            continue

        current_price = selected_stock["price"]
        if action == 'buy':
            market.portfolio.buy_stock(selected_stock["name"], current_price, quantity)
        elif action == 'sell':
            market.portfolio.sell_stock(selected_stock["name"], current_price, quantity)
    return True


def display_news(market):
    last_day_data = market.get_history()
    if last_day_data:
        news = last_day_data.get("news", {})
        event = last_day_data.get("event")
        print("\n📰 Today's Headlines:")
        print(f"   Headline: **{news.get('headline', 'N/A')}**")
        print(f"   Sentiment: {news.get('sentiment', 'N/A').upper()}")
        print(f"   Sector Focus: {news.get('sector', 'N/A').upper()}")
        if event:
            print(f"\n🚨 **MAJOR MARKET EVENT**: {event}")
        else:
            print("\n(No major market event active.)")
    else:
        print("No market history yet.")


def display_tips(market):
    active_tips = market.get_active_tips()
    if active_tips:
        print("\n🔔 Active Insider Tips (Resolve on Next Day):")
        for tip_data in active_tips:
            tip = tip_data["tip"]
            print(f" - [{tip['stock']}] {tip['message']}")
    else:
        print("\n🔔 No active insider tips currently.")


def save_load_menu(market):
    print("\n💾 Save/Load Functionality is a future feature.")


def main_menu(market):
    while True:
        print("\n======================================")
        print(f"     STOCK SIMULATOR - DAY {market.day}")
        print("======================================")
        print("1. View Market")
        print("2. Buy/Sell Stocks")
        print("3. Portfolio")
        print("4. Read News")
        print("5. Insider Tips")
        print("6. Advance Day")
        print("7. Save/Load Game")
        print("8. Exit")
        
        choice = input("Select an option (1-8): ").strip()
        if choice == '1':
            display_stocks(market)
        elif choice == '2':
            trade_menu(market)
        elif choice == '3':
            market.portfolio.summary(market.get_stocks())
        elif choice == '4':
            display_news(market)
        elif choice == '5':
            display_tips(market)
        elif choice == '6':
            print("Advancing to the next market day...")
            break
        elif choice == '7':
            save_load_menu(market)
        elif choice == '8':
            print(f"👋 Game Over. Final Portfolio Value: ₹{market.portfolio.get_portfolio_value(market.get_stocks()):,.2f}")
            sys.exit()
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


# -----------------------------
# MAIN GAME LOOP (with events)
# -----------------------------
if __name__ == "__main__":
    try:
        market = Market()
        print("Welcome to the Stock Market Simulator!")
        print(f"Starting balance: ₹{market.portfolio.balance:,.2f}")

        market.next_day()

        while True:
            main_menu(market)

            # ✅ NEW EVENT LOGIC (no class version)
            event = trigger_event({"stocks": market.get_stocks()}, market.day)
            if event:
                print(f"🚨 Major Event: {event['description']} affecting {event['sector']} sector!")

            # Continue to next day
            market.next_day()

    except FileNotFoundError as e:
        print(f"\nCRITICAL ERROR: {e}. Please ensure you have all necessary data files.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
