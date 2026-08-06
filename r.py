import json
import os

# Sample Dataset
TRAIN_DATA = [
    {"train_num": "12626", "route": "New Delhi - Trivandrum", "total_seats": 1000, "booked_seats": 980, "waiting_count": 45, "fare": 850.0, "cancellations": 30, "distance": 3034},
    {"train_num": "12952", "route": "Mumbai - New Delhi", "total_seats": 1200, "booked_seats": 1200, "waiting_count": 110, "fare": 1200.0, "cancellations": 15, "distance": 1386},
    {"train_num": "12302", "route": "New Delhi - Howrah", "total_seats": 900, "booked_seats": 890, "waiting_count": 60, "fare": 1050.0, "cancellations": 25, "distance": 1447},
    {"train_num": "12658", "route": "Bangalore - Chennai", "total_seats": 800, "booked_seats": 380, "waiting_count": 0, "fare": 350.0, "cancellations": 12, "distance": 362},
    {"train_num": "22691", "route": "Bangalore - Delhi", "total_seats": 1100, "booked_seats": 1050, "waiting_count": 20, "fare": 1500.0, "cancellations": 40, "distance": 2365},
    {"train_num": "12002", "route": "New Delhi - Bhopal", "total_seats": 700, "booked_seats": 320, "waiting_count": 0, "fare": 600.0, "cancellations": 5, "distance": 708}
]

def analyze_railway_revenue(trains):
    analytics_report = []
    
    print("--- Running Railway Reservation & Revenue Optimization Analysis ---")
    
    for t in trains:
        # 1. Calculate occupancy ratio
        # Occupancy Ratio = Booked Seats / Total Seats
        occupancy_ratio = round((t["booked_seats"] / t["total_seats"]) * 100, 2)
        
        # 2. Calculate actual revenue after cancellations
        # Active paid travelers = Booked Seats - Cancellations
        active_passengers = t["booked_seats"] - t["cancellations"]
        actual_revenue = active_passengers * t["fare"]
        
        # 3. Identify overbooked or high-demand trains
        # Flagged YES if waiting list count > 0 or occupancy ratio reaches 100%
        high_demand = "YES" if t["waiting_count"] > 0 or occupancy_ratio >= 100.0 else "NO"
        
        # 4. Calculate revenue per kilometer
        rev_per_km = round(actual_revenue / t["distance"], 2) if t["distance"] > 0 else 0.0
        
        analytics_report.append({
            "Train Number": t["train_num"],
            "Route": t["route"],
            "Occupancy Ratio (%)": occupancy_ratio,
            "Actual Revenue ($)": actual_revenue,
            "High Demand": high_demand,
            "Revenue Per KM ($)": rev_per_km,
            "Total Seats": t["total_seats"],
            "Booked Seats": t["booked_seats"]
        })
    
    # 5. Find the route with maximum revenue
    max_rev_train = max(analytics_report, key=lambda x: x["Actual Revenue ($)"])
    print(f"Route with Maximum Revenue: {max_rev_train['Route']} (${max_rev_train['Actual Revenue ($)']})")
    
    # 6. Display trains with occupancy below 50%
    print("\nTrains with Occupancy Below 50%:")
    low_occupancy_found = False
    for r in analytics_report:
        if r["Occupancy Ratio (%)"] < 50.0:
            print(f" - Train {r['Train Number']} ({r['Route']}) | Occupancy: {r['Occupancy Ratio (%)']}%")
            low_occupancy_found = True
    if not low_occupancy_found:
        print(" - None")
        
    # 7. Sort trains by revenue
    analytics_report.sort(key=lambda x: x["Actual Revenue ($)"], reverse=True)
    
    return analytics_report

def save_report_to_file(data, filename="railway_analytics.json"):
    # 8 & 9. Generate and save the reservation analytics report to file
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"\nSuccessfully generated and saved report to '{filename}'")

def read_and_display_top_three(filename="railway_analytics.json"):
    # 9 & 10. Read the report from file and display top three revenue-generating trains
    print("\n--- Top 3 Highest Revenue Generating Trains ---")
    if not os.path.exists(filename):
        print("Error: Report data file not found.")
        return
        
    with open(filename, "r", encoding="utf-8") as file:
        records = json.load(file)
    
    # Double check sort health order
    records.sort(key=lambda x: x["Actual Revenue ($)"], reverse=True)
    
    for i, record in enumerate(records[:3], 1):
        print(f"{i}. Train {record['Train Number']} | Route: {record['Route']}")
        print(f"   Revenue: ${record['Actual Revenue ($)']} | Occupancy: {record['Occupancy Ratio (%)']}% | Rev/KM: ${record['Revenue Per KM ($)']}")

if __name__ == "__main__":
    report_data = analyze_railway_revenue(TRAIN_DATA)
    save_report_to_file(report_data)
    read_and_display_top_three()
