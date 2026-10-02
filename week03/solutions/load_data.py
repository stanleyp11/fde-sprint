import csv
import os
from pathlib import Path

import psycopg

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://fde:fde@localhost:5432/o2c")
ROOT = Path(__file__).resolve().parents[2]

TABLES = {
    "accounts": ("accounts.csv", {
        "id": "id", "accountNumber": "account_number", "name": "name", "currency": "currency",
        "billToEmail": "bill_to_email", "stripeCustomerId": "stripe_customer_id", "status": "status"}),
    "subscriptions": ("subscriptions.csv", {
        "id": "id", "subscriptionNumber": "subscription_number", "accountNumber": "account_number",
        "status": "status", "productName": "product_name", "ratePlanName": "rate_plan_name",
        "quantity": "quantity", "listPricePerUnit": "list_price_per_unit",
        "discountPercent": "discount_percent", "billingPeriod": "billing_period",
        "termStartDate": "term_start_date", "termEndDate": "term_end_date", "mrr": "mrr"}),
    "invoices": ("invoices.csv", {
        "id": "id", "invoiceNumber": "invoice_number", "accountNumber": "account_number",
        "invoiceDate": "invoice_date", "dueDate": "due_date", "amount": "amount",
        "balance": "balance", "currency": "currency", "status": "status"}),
    "stripe_charges": ("stripe_charges.csv", {
        "id": "id", "customer": "customer", "amount_cents": "amount_cents", "currency": "currency",
        "created": "created", "status": "status", "description": "description",
        "metadata_invoice_number": "metadata_invoice_number"}),
}


def main():
    with psycopg.connect(DATABASE_URL) as conn:
        print("connected")
        schema = (Path(__file__).parent / "schema.sql").read_text()
        exists = conn.execute("SELECT to_regclass('public.accounts')").fetchone()[0]
        if not exists:
            conn.execute(schema)
        for table, (fname, cols) in TABLES.items():
            db_cols = list(cols.values())
            sql = (f"INSERT INTO {table} ({', '.join(db_cols)}) VALUES "
                   f"({', '.join(['%s'] * len(db_cols))}) ON CONFLICT (id) DO NOTHING")
            with open(ROOT / "data" / fname, newline="") as f:
                rows = [[r[k] or None for k in cols] for r in csv.DictReader(f)]
            with conn.cursor() as cur:
                cur.executemany(sql, rows)
        for table in TABLES:
            n = conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            print(f"{table:<16}{n:>5} rows")


if __name__ == "__main__":
    main()
