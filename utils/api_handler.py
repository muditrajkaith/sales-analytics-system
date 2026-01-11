# pip install requests


# Task 3.1 (a) Fetch All Products

def fetch_all_products():
    import requests
    
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url)
        print("Status Code:", response.status_code)
        
        data = response.json()
        print("Keys in response:", data.keys())
        
        print("API Fetch Successful")
        return data["products"]

    except Exception as e:
        print("API Fetch Failed:", e)
        return []


# Task 3.1 (b) Create Product Mapping

def create_product_mapping(api_products):

    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")

        if product_id is None:
            continue  # skip invalid API records

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),     # may be None
            "rating": product.get("rating")
        }

    return product_mapping




# Task 3.2 (a) Enrich Sales Data

def enrich_sales_data(transactions, product_mapping):
    enriched = []

    for t in transactions:
        new_t = t.copy()

        try:
            product_id = int(t["ProductID"][1:])
        except:
            product_id = None

        if product_id and product_id in product_mapping:
            api_data = product_mapping[product_id]
            new_t["API_Category"] = api_data.get("category")
            new_t["API_Brand"] = api_data.get("brand")
            new_t["API_Rating"] = api_data.get("rating")
            new_t["API_Match"] = True
        else:
            new_t["API_Category"] = None
            new_t["API_Brand"] = None
            new_t["API_Rating"] = None
            new_t["API_Match"] = False

        enriched.append(new_t)

    save_enriched_data(enriched)
    return enriched




def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    with open(filename, "w", encoding="utf-8") as f:

        header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
        f.write(header)

        for t in enriched_transactions:
            line = (
                f"{t['TransactionID']}|{t['Date']}|{t['ProductID']}|{t['ProductName']}|"
                f"{t['Quantity']}|{t['UnitPrice']}|{t['CustomerID']}|{t['Region']}|"
                f"{t['API_Category']}|{t['API_Brand']}|{t['API_Rating']}|{t['API_Match']}\n"
            )
            f.write(line)

    print("Enriched file saved successfully.")
