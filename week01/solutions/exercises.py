"""Reference solutions for week01/exercises.py. Try first, then compare."""


def format_currency(amount):
    sign = "-" if amount < 0 else ""
    return f"{sign}${abs(amount):,.2f}"


def annual_to_monthly(annual_price):
    return round(annual_price / 12, 2)


def apply_discount(price, percent):
    if percent < 0 or percent > 100:
        raise ValueError(f"discount percent must be 0-100, got {percent}")
    return round(price * (1 - percent / 100), 2)


def total_by_customer(invoices):
    totals = {}
    for row in invoices:
        totals[row["customer"]] = totals.get(row["customer"], 0) + row["amount"]
    return totals


def overdue_invoice_numbers(invoices, today):
    return [r["number"] for r in invoices if r["due_date"] < today and r["balance"] > 0]


def normalize_email(email):
    return email.strip().lower()


def parse_plan_code(code):
    parts = code.split("-")
    if len(parts) != 3:
        raise ValueError(f"expected TIER-TERM-CURRENCY, got {code!r}")
    tier, term, currency = parts
    return {"tier": tier, "term": term, "currency": currency}


def total_mrr(subscriptions):
    total = 0.0
    for s in subscriptions:
        per_period = s["unit_price"] * s["quantity"]
        total += per_period / 12 if s["period"] == "Annual" else per_period
    return round(total, 2)


def ramp_schedule(start_price, increase_percent, years):
    prices, price = [], start_price
    for _ in range(years):
        prices.append(round(price, 2))
        price = price * (1 + increase_percent / 100)
    return prices


def top_customers(totals, n):
    return sorted(totals, key=totals.get, reverse=True)[:n]
