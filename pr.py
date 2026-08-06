import csv
import os

# Sample Dataset with mock 3-month demand values inside the brackets []
PRODUCTS_DATA = [
    {"id": "P001", "name": "Wireless Mouse", "category": "Electronics", "opening_stock": 150, "units_sold": 120, "units_returned": 5, "lead_time": 5, "unit_cost": 15.0, "selling_price": 30.0, "past_demand": [110, 130, 125]},
    {"id": "P002", "name": "Ergonomic Chair", "category": "Furniture", "opening_stock": 40, "units_sold": 35, "units_returned": 2, "lead_time": 14, "unit_cost": 80.0, "selling_price": 150.0, "past_demand": [30, 42, 38]},
    {"id": "P003", "name": "Bluetooth Speaker", "category": "Electronics", "opening_stock": 80, "units_sold": 75, "units_returned": 8, "lead_time": 7, "unit_cost": 25.0, "selling_price": 50.0, "past_demand": [70, 85, 72]},
    {"id": "P004", "name": "Running Shoes", "category": "Apparel", "opening_stock": 200, "units_sold": 180, "units_returned": 12, "lead_time": 10, "unit_cost": 40.0, "selling_price": 90.0, "past_demand": [160, 190, 175]},
    {"id": "P005", "name": "Coffee Maker", "category": "Appliances", "opening_stock": 30, "units_sold": 28, "units_returned": 1, "lead_time": 6, "unit_cost": 60.0, "selling_price": 120.0, "past_demand": [25, 30, 27]},
    {"id": "P006", "name": "Desk Lamp", "category": "Furniture", "opening_stock": 100, "units_sold": 40, "units_returned": 0, "lead_time": 4, "unit_cost": 10.0, "selling_price": 25.0, "past_demand":}
]

def analyze_inventory(products):
    processed_list = []
    category_profit = {}
    
    print("--- Running Inventory Analysis ---")
    
    for p in products:
        # 1. Calculate current stock
        net_sold = p["units_sold"] - p["units_returned"]
        current_stock = p["opening_stock"] - net_sold
        
        # 2. Calculate profit for each product
        total_revenue = net_sold * p["selling_price"]
        total_cost = (p["opening_stock"] * p["unit_cost"]) - (current_stock * p["unit_cost"])
        profit = total_revenue - total_cost
        
        # 3. Identify products requiring immediate reorder
        avg_past_demand = sum(p["past_demand"]) / len(p["past_demand"])
        daily_demand = avg_past_demand / 30
        reorder_point = daily_demand * p["lead_time"]
        needs_reorder = "YES" if current_stock <= reorder_point else "NO"
        
        # 4. Compute inventory turnover ratio
        avg_inventory_units = (p["opening_stock"] + current_stock) / 2
        cogs = net_sold * p["unit_cost"]
        avg_inventory_value = avg_inventory_units * p["unit_cost"]
        inventory_turnover = round(cogs / avg_inventory_value, 2) if avg_inventory_value > 0 else 0.0
        
        # 6. Accumulate category-wise profit
        category_profit[p["category"]] = category_profit.get(p["category"], 0.0) + profit
        
        # 7. Predict next month demand using moving average logic
        predicted_demand = round(avg_past_demand, 1)
        
        processed_list.append({
            "Product ID": p["id"],
            "Product Name": p["name"],
            "Category": p["category"],
            "Current Stock": current_stock,
            "Profit": round(profit, 2),
            "Needs Reorder": needs_reorder,
            "Inventory Turnover Ratio": inventory_turnover,
            "Predicted Demand": predicted_demand
        })
        
    # 5. Find the highest profit product
    highest_profit_prod = max(processed_list, key=lambda x: x["Profit"])
    print(f"Highest Profit Product: {highest_profit_prod['Product Name']} (${highest_profit_prod['Profit']})")
    
    print("\nCategory-Wise Profit Distribution:")
    for cat, prof in category_profit.items():
        print(f" - {cat}: ${round(prof, 2)}")
        
    # 8. Sort products by profitability
    processed_list.sort(key=lambda x: x["Profit"], reverse=True)
    
    return processed_list

def export_to_csv(data, filename="inventory_report.csv"):
    # 9. Export inventory report to CSV
    fields = ["Product ID", "Product Name", "Category", "Current Stock", "Profit", "Needs Reorder", "Inventory Turnover Ratio", "Predicted Demand"]
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
    print(f"\nSuccessfully exported report to '{filename}'")

def read_and_display_top_five(filename="inventory_report.csv"):
    # 10. Read the CSV and display the top five profitable products
    print("\n--- Top 5 Most Profitable Products (Read from CSV) ---")
    if not os.path.exists(filename):
        print("Error: Report file not found.")
        return
        
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        
    rows.sort(key=lambda x: float(x["Profit"]), reverse=True)
    
    for i, row in enumerate(rows[:5], 1):
        print(f"{i}. {row['Product Name']} ({row['Category']}) | Profit: ${row['Profit']} | Stock: {row['Current Stock']} | Predicted Demand: {row['Predicted Demand']}")

if __name__ == "__main__":
    analyzed_data = analyze_inventory(PRODUCTS_DATA)
    export_to_csv(analyzed_data)
    read_and_display_top_five()
