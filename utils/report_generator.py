
import os
from datetime import datetime


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):

    os.makedirs("output", exist_ok=True)

    total_transactions = len(transactions)

    # Overall Summary
    total_revenue = sum(t["Quantity"] * t["UnitPrice"] for t in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [t["Date"] for t in transactions]
    start_date = min(dates)
    end_date = max(dates)

    # Region Performance
    region_stats = {}
    for t in transactions:
        region = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        if region not in region_stats:
            region_stats[region] = {"sales": 0, "count": 0}

        region_stats[region]["sales"] += amount
        region_stats[region]["count"] += 1

    # sort regions by sales descending
    region_stats = dict(sorted(region_stats.items(),
                               key=lambda x: x[1]["sales"],
                               reverse=True))

    # Product Performance
    product_stats = {}
    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_stats:
            product_stats[name] = {"qty": 0, "revenue": 0}

        product_stats[name]["qty"] += qty
        product_stats[name]["revenue"] += revenue

    # Top 5 products
    top_products = sorted(product_stats.items(),
                          key=lambda x: x[1]["qty"],
                          reverse=True)[:5]

    # Low performing products (qty < 10)
    low_products = [(name, stats["qty"], stats["revenue"])
                    for name, stats in product_stats.items()
                    if stats["qty"] < 10]

    low_products.sort(key=lambda x: x[1])

    # Customer Performance
    customer_stats = {}
    for t in transactions:
        cid = t["CustomerID"]
        amount = t["Quantity"] * t["UnitPrice"]

        if cid not in customer_stats:
            customer_stats[cid] = {"spent": 0, "orders": 0}

        customer_stats[cid]["spent"] += amount
        customer_stats[cid]["orders"] += 1

    top_customers = sorted(customer_stats.items(),
                            key=lambda x: x[1]["spent"],
                            reverse=True)[:5]

    # Daily Trend
    daily_stats = {}
    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]
        cid = t["CustomerID"]

        if date not in daily_stats:
            daily_stats[date] = {"revenue": 0, "transactions": 0, "customers": set()}

        daily_stats[date]["revenue"] += amount
        daily_stats[date]["transactions"] += 1
        daily_stats[date]["customers"].add(cid)

    daily_stats = dict(sorted(daily_stats.items()))

    # API Enrichment
    enriched_count = sum(1 for t in enriched_transactions if t["API_Match"])
    success_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

    failed_products = list(set(
        t["ProductName"] for t in enriched_transactions if not t["API_Match"]
    ))

    # Write Report
    with open(output_file, "w") as file:

        file.write("SALES ANALYTICS REPORT\n")
        file.write("=" * 50 + "\n")
        file.write(f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Records Processed: {total_transactions}\n\n")

        # Overall Summary
        file.write("OVERALL SUMMARY\n")
        file.write("-" * 50 + "\n")
        file.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        file.write(f"Total Transactions: {total_transactions}\n")
        file.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        file.write(f"Date Range: {start_date} to {end_date}\n\n")

        # Region Performance
        file.write("REGION-WISE PERFORMANCE\n")
        file.write("-" * 50 + "\n")
        file.write("Region | Total Sales | % of Transactions\n")

        for region, stats in region_stats.items():
            percent = (stats["count"] / total_transactions) * 100
            file.write(f"{region} | ₹{stats['sales']:,.2f} | {percent:.2f}%\n")

        file.write("\n")

        # Top Products
        file.write("TOP PRODUCTS\n")
        file.write("-" * 50 + "\n")
        file.write("Rank | Product | Quantity Sold | Revenue\n")

        for i, (name, stats) in enumerate(top_products, 1):
            file.write(f"{i} | {name} | {stats['qty']} | ₹{stats['revenue']:,.2f}\n")

        file.write("\n")

        # Top Customers
        file.write("TOP CUSTOMERS\n")
        file.write("-" * 50 + "\n")
        file.write("Rank | CustomerID | Total Spent | Orders\n")

        for i, (cid, stats) in enumerate(top_customers, 1):
            file.write(f"{i} | {cid} | ₹{stats['spent']:,.2f} | {stats['orders']}\n")

        file.write("\n")

        # Daily Trend
        file.write("DAILY SALES TREND\n")
        file.write("-" * 50 + "\n")
        file.write("Date | Revenue | Transactions | Unique Customers\n")

        for date, stats in daily_stats.items():
            file.write(f"{date} | ₹{stats['revenue']:,.2f} | {stats['transactions']} | {len(stats['customers'])}\n")

        file.write("\n")

        # Product Performance
        file.write("PRODUCT PERFORMANCE ANALYSIS\n")
        file.write("-" * 50 + "\n")

        if low_products:
            file.write("Low Performing Products:\n")
            for name, qty, revenue in low_products:
                file.write(f"{name} - Qty: {qty}, Revenue: ₹{revenue:,.2f}\n")
        else:
            file.write("No low performing products found.\n")

        file.write("\n")

        # API Summary
        file.write("API ENRICHMENT SUMMARY\n")
        file.write("-" * 50 + "\n")
        file.write(f"Total Records Enriched: {enriched_count}\n")
        file.write(f"Success Rate: {success_rate:.2f}%\n")

        if failed_products:
            file.write("Products Not Enriched:\n")
            for p in failed_products:
                file.write(f"- {p}\n")

    print(f"Sales report generated successfully: {output_file}")


