import csv

INPUT_PATH = "sample_data/sales_messy.csv"
OUTPUT_PATH = "output/clean_sales.csv"


def main():
    # Naive pipeline (intentionally broken):
    # - assumes comma delimiter
    # - assumes fixed column names
    # - assumes numeric fields are always valid
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # default delimiter is ","
        rows = list(reader)

    cleaned = []
    for row in rows:
        order_id = int(row["Order ID"])
        order_date = row["Order Date"]
        customer = row["Customer Name"]
        product = row["Product"]

        amount = float(row["Amount"])      # breaks on "$19,99", "USD 12.50", ""
        quantity = int(row["Quantity"])    # breaks on "", "two"

        cleaned.append([order_id, order_date, customer, product, amount, quantity])

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["order_id", "order_date", "customer", "product", "amount", "quantity"])
        writer.writerows(cleaned)


if __name__ == "__main__":
    main()
