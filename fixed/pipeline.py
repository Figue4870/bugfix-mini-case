import csv
import re
from pathlib import Path
from datetime import datetime

INPUT_PATH = Path("sample_data") / "sales_messy.csv"
OUTPUT_DIR = Path("output")
OUTPUT_PATH = OUTPUT_DIR / "clean_sales.csv"


def parse_date(value):
    value = (value or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return ""


def parse_amount(value):
    value = (value or "").strip()
    if value == "":
        return ""

    value = value.replace("USD", "").replace("$", "").strip()
    value = value.replace(",", ".")
    value = re.sub(r"[^\d.]", "", value)

    try:
        return f"{float(value):.2f}" if value != "" else ""
    except ValueError:
        return ""


def parse_int(value):
    value = (value or "").strip()
    try:
        return str(int(value)) if value != "" else ""
    except ValueError:
        return ""


def detect_dialect(text):
    sniffer = csv.Sniffer()
    try:
        return sniffer.sniff(text, delimiters=[",", ";", "\t", "|"])
    except csv.Error:
        dialect = csv.excel
        dialect.delimiter = ";"
        return dialect


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        content = INPUT_PATH.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = INPUT_PATH.read_text(encoding="latin-1")

    dialect = detect_dialect(content[:2048])
    reader = csv.DictReader(content.splitlines(), dialect=dialect)

    if reader.fieldnames:
        reader.fieldnames = [h.strip() for h in reader.fieldnames]

    rows = []
    for row in reader:
        normalized = {}
        for k, v in row.items():
            if k is not None:
                normalized[k.strip()] = (v or "").strip()

        rows.append({
            "order_id": parse_int(normalized.get("Order ID", "")),
            "order_date": parse_date(normalized.get("Order Date", "")),
            "customer": normalized.get("Customer Name", ""),
            "product": normalized.get("Product", ""),
            "amount": parse_amount(normalized.get("Amount", "")),
            "quantity": parse_int(normalized.get("Quantity", "")),
        })

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["order_id", "order_date", "customer", "product", "amount", "quantity"],)
        writer.writeheader()
        writer.writerows(rows)


main()
