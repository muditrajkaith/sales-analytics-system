
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data
from utils.report_generator import generate_sales_report


def main():
    try:
        print("\n==============================")
        print("      SALES ANALYTICS SYSTEM")
        print("==============================\n")

        # 1. Read sales data
        print("[1/10] Reading sales data...")
        lines = read_sales_data("data/sales_data.txt")
        print(f"✔ Successfully read {len(lines)} records\n")

        # 2. Parse & clean data
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(lines)
        print(f"✔ Parsed {len(transactions)} records\n")

        # 3. Show filter options
        regions = sorted(set(t["Region"] for t in transactions))
        amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]

        print("[3/10] Filter Options Available:")
        print("Regions:", ", ".join(regions))
        print(f"Amount Range: {int(min(amounts))} - {int(max(amounts))}\n")

        # 4. Ask user for filters
        choice = input("Do you want to filter data? (y/n): ").strip().lower()

        region = None
        min_amt = None
        max_amt = None

        if choice == "y":
            region = input("Enter region (or press Enter to skip): ").strip()
            region = region if region else None

            min_amt = input("Enter minimum amount (or press Enter to skip): ").strip()
            min_amt = float(min_amt) if min_amt else None

            max_amt = input("Enter maximum amount (or press Enter to skip): ").strip()
            max_amt = float(max_amt) if max_amt else None

        # 5. Validate transactions
        print("\n[4/10] Validating transactions...")
        valid_tx, invalid_count, summary = validate_and_filter(
            transactions, region, min_amt, max_amt
        )

        print(f"✔ Valid: {len(valid_tx)} | Invalid: {invalid_count}\n")

        # 6. Perform analytics (Part 2)
        print("[5/10] Analyzing sales data...")

        total_revenue = calculate_total_revenue(valid_tx)
        region_stats = region_wise_sales(valid_tx)
        top_products = top_selling_products(valid_tx)
        customers = customer_analysis(valid_tx)
        daily_trend = daily_sales_trend(valid_tx)
        peak_day = find_peak_sales_day(valid_tx)
        low_products = low_performing_products(valid_tx)

        print("✔ Analysis complete\n")

        # 7. Fetch API data
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✔ Fetched {len(api_products)} products\n")

        # 8. Create product mapping
        print("[7/10] Creating product mapping...")
        product_mapping = create_product_mapping(api_products)
        print("✔ Product mapping created\n")

        # 9. Enrich transactions
        print("[8/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_tx, product_mapping)
        matched = sum(1 for t in enriched_transactions if t["API_Match"])
        print(f"✔ Enriched {matched} records ({round(matched/len(enriched_transactions)*100,2)}%)\n")

        # 10. Generate report
        print("[9/10] Generating report...")
        generate_sales_report(valid_tx, enriched_transactions)
        print("✔ Report saved to output/sales_report.txt\n")

        print("[10/10] Process Complete!")
        print("==============================")
        print("Pipeline executed successfully")
        print("==============================")

    except Exception as e:
        print("\n❌ ERROR OCCURRED")
        print("Reason:", str(e))
        print("Pipeline terminated.")


if __name__ == "__main__":
    main()
