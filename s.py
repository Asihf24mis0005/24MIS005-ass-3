import json
import os

# Sample Dataset containing portfolio holdings across investors
PORTFOLIO_DATA = [
    {"investor_id": "INV001", "symbol": "AAPL", "quantity": 50, "buy_price": 150.0, "current_price": 180.0, "sector": "Technology", "dividend": 120.0},
    {"investor_id": "INV001", "symbol": "JPM", "quantity": 30, "buy_price": 130.0, "current_price": 145.0, "sector": "Finance", "dividend": 90.0},
    {"investor_id": "INV002", "symbol": "TSLA", "quantity": 20, "buy_price": 250.0, "current_price": 190.0, "sector": "Automotive", "dividend": 0.0},
    {"investor_id": "INV002", "symbol": "NVDA", "quantity": 40, "buy_price": 400.0, "current_price": 850.0, "sector": "Technology", "dividend": 15.0},
    {"investor_id": "INV003", "symbol": "XOM", "quantity": 100, "buy_price": 90.0, "current_price": 115.0, "sector": "Energy", "dividend": 340.0},
    {"investor_id": "INV003", "symbol": "PFE", "quantity": 150, "buy_price": 40.0, "current_price": 28.0, "sector": "Healthcare", "dividend": 260.0}
]

def analyze_portfolio(records):
    analyzed_stocks = []
    sector_values = {}
    investor_aggregates = {}
    total_current_market_value = 0.0
    
    print("--- Running Stock Portfolio & Risk Analysis ---")
    
    for r in records:
        # Core Calculations per stock holding
        investment_value = r["quantity"] * r["buy_price"]
        current_value = r["quantity"] * r["current_price"]
        profit_loss = current_value - investment_value
        
        # Percentage return inclusive of dividends received
        total_return_amount = profit_loss + r["dividend"]
        pct_return = round((total_return_amount / investment_value) * 100, 2) if investment_value > 0 else 0.0
        
        total_current_market_value += current_value
        
        # Track sector allocation values
        sector_values[r["sector"]] = sector_values.get(r["sector"], 0.0) + current_value
        
        # Aggregate tracking data sorted by individual investor
        if r["investor_id"] not in investor_aggregates:
            investor_aggregates[r["investor_id"]] = {"total_cost": 0.0, "total_value": 0.0, "total_div": 0.0}
        investor_aggregates[r["investor_id"]]["total_cost"] += investment_value
        investor_aggregates[r["investor_id"]]["total_value"] += current_value
        investor_aggregates[r["investor_id"]]["total_div"] += r["dividend"]
        
        analyzed_stocks.append({
            "Investor ID": r["investor_id"],
            "Stock Symbol": r["symbol"],
            "Sector": r["sector"],
            "Investment Value": round(investment_value, 2),
            "Current Value": round(current_value, 2),
            "Profit/Loss": round(profit_loss, 2),
            "Percentage Return (%)": pct_return
        })
        
    # Best and worst performing asset lookup strings
    best_stock = max(analyzed_stocks, key=lambda x: x["Percentage Return (%)"])
    worst_stock = min(analyzed_stocks, key=lambda x: x["Percentage Return (%)"])
    
    print(f"Best Performing Stock: {best_stock['Stock Symbol']} ({best_stock['Percentage Return (%)']}% Return)")
    print(f"Worst Performing Stock: {worst_stock['Stock Symbol']} ({worst_stock['Percentage Return (%)']}% Return)")
    
    # Calculate Sector Exposure percentage breakdown metrics
    print("\nSector-Wise Exposure Distribution:")
    sector_exposure = {}
    for sector, val in sector_values.items():
        exposure_pct = round((val / total_current_market_value) * 100, 2) if total_current_market_value > 0 else 0.0
        sector_exposure[sector] = exposure_pct
        print(f" - {sector}: {exposure_pct}% exposure")
        
    # Rank Investors by overall net aggregate portfolio returns
    investor_ranking = []
    for inv_id, metrics in investor_aggregates.items():
        net_gain = (metrics["total_value"] - metrics["total_cost"]) + metrics["total_div"]
        inv_pct_return = round((net_gain / metrics["total_cost"]) * 100, 2) if metrics["total_cost"] > 0 else 0.0
        investor_ranking.append({
            "Investor ID": inv_id,
            "Portfolio Return (%)": inv_pct_return
        })
    investor_ranking.sort(key=lambda x: x["Portfolio Return (%)"], reverse=True)
    
    # Bundle components cleanly inside a final structured master data payload
    report_payload = {
        "stock_metrics": analyzed_stocks,
        "sector_exposure": sector_exposure,
        "investor_rankings": investor_ranking
    }
    return report_payload

def save_report(data, filename="portfolio_report.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"\nReport generated successfully and saved to file: '{filename}'")

def read_and_display_report(filename="portfolio_report.json"):
    print("\n--- Reading Archived Portfolio Report File Data ---")
    if not os.path.exists(filename):
        print("Error: Targeted source file record path does not exist.")
        return
        
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("\nRanked Investors by Portfolio Return:")
    for rank, inv in enumerate(data["investor_rankings"], 1):
        print(f" Rank {rank}: Investor {inv['Investor ID']} | Net Return: {inv['Portfolio Return (%)']}%")

if __name__ == "__main__":
    final_report = analyze_portfolio(PORTFOLIO_DATA)
    save_report(final_report)
    read_and_display_report()
