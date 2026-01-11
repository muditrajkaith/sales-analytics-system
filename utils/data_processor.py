# Task 2.1 (a) Calculate Total Revenue

def calculate_total_revenue(transactions):
    total = 0
    for t in transactions:
        total += t["Quantity"] * t["UnitPrice"]
    return total



# Task 2.1 (b) Region-wise Sales Analysis

def region_wise_sales(transactions):
    region_data = {}

    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        region = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    # calculate percentage
    for region in region_data:
        sales = region_data[region]["total_sales"]
        percent = (sales / total_revenue) * 100
        region_data[region]["percentage"] = round(percent, 2)

    # sort by total_sales descending
    sorted_regions = dict(sorted(region_data.items(),
                                  key=lambda x: x[1]["total_sales"],
                                  reverse=True))

    return sorted_regions



# Task 2.1 (c) Top Selling Products

def top_selling_products(transactions, n=5):
    product_data = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_data:
            product_data[name] = {"qty": 0, "revenue": 0}

        product_data[name]["qty"] += qty
        product_data[name]["revenue"] += revenue

    result = []
    for name, data in product_data.items():
        result.append((name, data["qty"], data["revenue"]))

    result.sort(key=lambda x: x[1], reverse=True)
    return result[:n]


# Task 2.1 (d) Customer Purchase Analysis

def customer_analysis(transactions):
    customers = {}

    for t in transactions:
        cid = t["CustomerID"]
        amount = t["Quantity"] * t["UnitPrice"]

        if cid not in customers:
            customers[cid] = {
                "total_spent": 0,
                "purchase_count": 0,
                "products": set()
            }

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1
        customers[cid]["products"].add(t["ProductName"])

    result = {}

    for cid, data in customers.items():
        avg = data["total_spent"] / data["purchase_count"]

        result[cid] = {
            "total_spent": data["total_spent"],
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(avg, 2),
            "products_bought": list(data["products"])
        }

    # sort by total spent
    result = dict(sorted(result.items(),
                         key=lambda x: x[1]["total_spent"],
                         reverse=True))

    return result


# Task 2.2 (a) Daily Sales Trend

def daily_sales_trend(transactions):
    daily = {}

    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]

        if date not in daily:
            daily[date] = {
                "revenue": 0,
                "transaction_count": 0,
                "customers": set()
            }

        daily[date]["revenue"] += amount
        daily[date]["transaction_count"] += 1
        daily[date]["customers"].add(t["CustomerID"])

    result = {}
    for date in sorted(daily):
        result[date] = {
            "revenue": daily[date]["revenue"],
            "transaction_count": daily[date]["transaction_count"],
            "unique_customers": len(daily[date]["customers"])
        }

    return result


# Task 2.2 (b) Find Peak Sales Day

def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    max_date = None
    max_revenue = 0

    for date, data in daily.items():
        if data["revenue"] > max_revenue:
            max_revenue = data["revenue"]
            max_date = date
            max_count = data["transaction_count"]

    return (max_date, max_revenue, max_count)





# Task 2.3 (a) Low Performing Products

def low_performing_products(transactions, threshold=10):
    product_data = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_data:
            product_data[name] = {"qty": 0, "revenue": 0}

        product_data[name]["qty"] += qty
        product_data[name]["revenue"] += revenue

    result = []

    for name, data in product_data.items():
        if data["qty"] < threshold:
            result.append((name, data["qty"], data["revenue"]))

    result.sort(key=lambda x: x[1])
    return result

