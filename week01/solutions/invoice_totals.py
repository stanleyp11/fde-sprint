import csv
import sys

from exercises import format_currency, top_customers


def main(path):
    totals, skipped = {}, []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            number = row.get("invoice_number") or "?"
            if not row.get("customer") or row.get("amount") in (None, ""):
                skipped.append(f"{number} (missing fields)")
                continue
            try:
                amount = float(row["amount"])
            except ValueError:
                skipped.append(f"{number} (amount {row['amount']!r})")
                continue
            totals[row["customer"]] = totals.get(row["customer"], 0) + amount
    for name in top_customers(totals, len(totals)):
        print(f"{name:<22}{format_currency(totals[name]):>12}")
    if skipped:
        print(f"Skipped {len(skipped)} bad rows: " + ", ".join(skipped))


if __name__ == "__main__":
    main(sys.argv[1])
