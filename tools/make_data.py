"""Generate the synthetic O2C dataset used throughout the sprint.

Everything here is fake: company names, emails, amounts. Run it any time to
rebuild /data:  python tools/make_data.py

It plants known problems on purpose so your reconciliation work has
something real to find (see data/PLANTED_ISSUES.md after running).
"""
import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)
OUT = Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(exist_ok=True)

COMPANIES = [
    "Acme Analytics", "Bluefin Logistics", "Cedar Health", "Delta Robotics", "Evergreen Foods",
    "Falcon Security", "Granite Legal", "Harbor Media", "Ion Energy", "Juniper Retail",
    "Kestrel Labs", "Lumen Education", "Maple Insurance", "Nimbus Cloud", "Orbit Travel",
    "Pioneer Freight", "Quartz Finance", "Redwood Clinics", "Summit Sports", "Tidal Water",
    "Umber Design", "Vertex Mining", "Willow Pets", "Xenon Telecom", "Yarrow Farms",
]
PLANS = [
    # (product, rate plan, list price per unit per month, billing period)
    ("Platform", "Platform Starter Monthly", 25.0, "Month"),
    ("Platform", "Platform Pro Monthly", 60.0, "Month"),
    ("Platform", "Platform Pro Annual", 50.0, "Annual"),
    ("Platform", "Platform Enterprise Annual", 90.0, "Annual"),
]
CURRENCY = "USD"
START = date(2026, 1, 1)


def money(x):
    return round(x + 1e-9, 2)


accounts, subscriptions, invoices, charges = [], [], [], []
for i, name in enumerate(COMPANIES, start=1):
    acct_num = f"A{i:08d}"
    acct_id = f"8a8{i:05d}c0ffee{i:04d}"
    slug = name.lower().replace(" ", "")
    accounts.append({
        "id": acct_id, "accountNumber": acct_num, "name": name,
        "currency": CURRENCY, "billToEmail": f"ap@{slug}.example.com",
        "stripeCustomerId": f"cus_test{i:06d}", "status": "Active",
    })
    product, plan, unit, period = random.choice(PLANS)
    qty = random.choice([5, 10, 20, 25, 50, 100, 250])
    discount = random.choice([0, 0, 0, 10, 15, 20])
    sub_start = START + timedelta(days=random.randint(0, 120))
    term_months = 12 if period == "Annual" else random.choice([12, 24, 36])
    monthly = money(unit * qty * (1 - discount / 100))
    sub_num = f"S{i:08d}"
    subscriptions.append({
        "id": f"2c9{i:05d}5ub{i:04d}", "subscriptionNumber": sub_num, "accountNumber": acct_num,
        "status": "Active", "productName": product, "ratePlanName": plan,
        "quantity": qty, "listPricePerUnit": unit, "discountPercent": discount,
        "billingPeriod": period, "termStartDate": sub_start.isoformat(),
        "termEndDate": (sub_start + timedelta(days=30 * term_months)).isoformat(),
        "mrr": monthly,
    })
    # invoices: monthly plans -> one invoice per month through Sep 2026; annual -> one invoice
    if period == "Annual":
        bills = [(sub_start, money(monthly * 12))]
    else:
        bills, d = [], sub_start
        while d <= date(2026, 9, 1):
            bills.append((d, monthly))
            m = d.month + 1
            d = date(d.year + (m > 12), (m - 1) % 12 + 1, min(d.day, 28))
    for j, (inv_date, amt) in enumerate(bills, start=1):
        inv_num = f"INV{i:04d}{j:03d}"
        due = inv_date + timedelta(days=30)
        invoices.append({
            "id": f"inv{i:04d}{j:03d}", "invoiceNumber": inv_num, "accountNumber": acct_num,
            "invoiceDate": inv_date.isoformat(), "dueDate": due.isoformat(),
            "amount": amt, "balance": 0.0, "currency": CURRENCY, "status": "Posted",
        })
        pay_date = inv_date + timedelta(days=random.randint(1, 25))
        charges.append({
            "id": f"ch_test{i:04d}{j:03d}", "customer": f"cus_test{i:06d}",
            "amount_cents": int(round(amt * 100)), "currency": "usd",
            "created": pay_date.isoformat(), "status": "succeeded",
            "description": f"Payment for {inv_num}", "metadata_invoice_number": inv_num,
        })

# ---- planted issues (the reconciliation should find all of these) ----
planted = []
# 1. Amount mismatch: Stripe charged 10.00 less than the invoice
c = charges[7]
c["amount_cents"] -= 1000
planted.append(f"AMOUNT_MISMATCH: {c['metadata_invoice_number']} charged $10.00 less than invoiced ({c['id']})")
# 2. Missing payment: invoice has no charge, balance still open
inv = invoices[15]
charges = [x for x in charges if x["metadata_invoice_number"] != inv["invoiceNumber"]]
inv["balance"] = inv["amount"]
planted.append(f"MISSING_PAYMENT: {inv['invoiceNumber']} has no Stripe charge (open balance ${inv['amount']:.2f})")
# 3. Duplicate charge: customer charged twice for one invoice
dup = dict(charges[30])
dup["id"] = dup["id"] + "_dup"
charges.append(dup)
planted.append(f"DUPLICATE_CHARGE: {dup['metadata_invoice_number']} charged twice ({charges[30]['id']} and {dup['id']})")
# 4. Orphan charge: Stripe charge with no matching invoice
orphan = {"id": "ch_test9999001", "customer": "cus_test000004", "amount_cents": 4999, "currency": "usd",
          "created": "2026-07-14", "status": "succeeded", "description": "Manual charge",
          "metadata_invoice_number": ""}
charges.append(orphan)
planted.append("ORPHAN_CHARGE: ch_test9999001 ($49.99) has no invoice reference")
# 5. Failed charge: payment attempt failed, invoice still open
fc = charges[45]
fc["status"] = "failed"
inv_fc = next(x for x in invoices if x["invoiceNumber"] == fc["metadata_invoice_number"])
inv_fc["balance"] = inv_fc["amount"]
planted.append(f"FAILED_PAYMENT: {fc['metadata_invoice_number']} payment {fc['id']} failed; balance open")
# 6. Overdue open invoice is item 2 and 5 as well (dueDate in the past with balance > 0)


def write_csv(name, rows):
    with open(OUT / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


write_csv("accounts.csv", accounts)
write_csv("subscriptions.csv", subscriptions)
write_csv("invoices.csv", invoices)
write_csv("stripe_charges.csv", charges)
(OUT / "zuora_dataset.json").write_text(json.dumps(
    {"accounts": accounts, "subscriptions": subscriptions, "invoices": invoices}, indent=2))
(OUT / "PLANTED_ISSUES.md").write_text(
    "# Planted issues (answer key)\n\nTry to find these with your own code before reading this file.\n\n"
    + "\n".join(f"- {p}" for p in planted) + "\n")
print(f"{len(accounts)} accounts, {len(subscriptions)} subscriptions, {len(invoices)} invoices, {len(charges)} charges")
for p in planted:
    print(" -", p)
