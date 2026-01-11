def read_sales_data(filename):
    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                lines = file.readlines()

            # Remove header and empty lines
            clean_lines = []
            for line in lines[1:]:   # skip header
                line = line.strip()
                if line != "":
                    clean_lines.append(line)

            return clean_lines

        except FileNotFoundError:
            print("File not found:", filename)
            return []

        except:
            # Try next encoding
            continue

    print("Unable to read file with supported encodings")
    return []


def parse_transactions(raw_lines):

    transactions = []

    for line in raw_lines:
        fields = line.split('|')

        # Skip incorrect number of fields
        if len(fields) != 8:
            continue

        transaction_id = fields[0]
        date = fields[1]
        product_id = fields[2]
        product_name = fields[3]
        quantity = fields[4]
        unit_price = fields[5]
        customer_id = fields[6]
        region = fields[7]

        # Clean commas in product name
        product_name = product_name.replace(",", "")

        # Clean numeric fields
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except:
            continue

        transaction = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        transactions.append(transaction)

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    total_input = len(transactions)

    # Display available regions
    regions = set()
    amounts = []

    for tx in transactions:
        regions.add(tx["Region"])
        amounts.append(tx["Quantity"] * tx["UnitPrice"])

    print("Available regions:", list(regions))
    print("Transaction amount range:", min(amounts), "-", max(amounts))

    for tx in transactions:
        # Validation rules
        if tx["Quantity"] <= 0 or tx["UnitPrice"] <= 0:
            invalid_count += 1
            continue

        if not tx["TransactionID"].startswith("T"):
            invalid_count += 1
            continue

        if not tx["ProductID"].startswith("P"):
            invalid_count += 1
            continue

        if not tx["CustomerID"].startswith("C"):
            invalid_count += 1
            continue

        amount = tx["Quantity"] * tx["UnitPrice"]

        # Apply filters
        if region is not None and tx["Region"] != region:
            continue

        if min_amount is not None and amount < min_amount:
            continue

        if max_amount is not None and amount > max_amount:
            continue

        valid_transactions.append(tx)

    filter_summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": region,
        "filtered_by_amount": {
            "min": min_amount,
            "max": max_amount
        },
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, filter_summary
