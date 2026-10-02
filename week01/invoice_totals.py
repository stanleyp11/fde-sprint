"""Week 1, Thursday: read a CSV and total invoices by customer.

Your task: write main() so that
    python week01/invoice_totals.py week01/data/invoices_small.csv
prints one line per customer, highest total first, like:

    Cedar Health          $6,125.00
    Ion Energy            $6,000.00
    ...
    Skipped 2 bad rows: INV-1012 (amount 'not-a-number'), INV-1018 (missing fields)

Rules:
  - Use the csv module (csv.DictReader).
  - A row with a missing field or a non-numeric amount is skipped and reported,
    never crashes the script.
  - Reuse format_currency and top_customers from exercises.py.

Steps:
  1. Open the file and print every row. Run it.
  2. Convert amount with float() inside try/except ValueError.
  3. Build the totals dict.
  4. Sort and print. Then print the skipped rows.
"""
import sys


def main(path):
    raise NotImplementedError


if __name__ == "__main__":
    main(sys.argv[1])
