"""Week 1, Tuesday: Python basics with billing flavor.

How to work:
  1. Read the docstring of each function.
  2. Replace `raise NotImplementedError` with your code.
  3. Run:  pytest week01/tests/test_exercises.py -v
  4. Fix until all 10 tests pass. Commit after each one that turns green.

Don't look in week01/solutions/ until you have tried for 20 minutes.
"""


def format_currency(amount):
    """Return amount as US dollars with commas and 2 decimals.

    format_currency(1234.5)  -> "$1,234.50"
    format_currency(-20)     -> "-$20.00"
    Hint: f"{x:,.2f}" adds commas and 2 decimals.
    """
    raise NotImplementedError


def annual_to_monthly(annual_price):
    """Monthly equivalent of an annual price, rounded to 2 decimals.

    annual_to_monthly(1200) -> 100.0
    annual_to_monthly(1000) -> 83.33
    """
    raise NotImplementedError


def apply_discount(price, percent):
    """Price after a percent discount, rounded to 2 decimals.

    apply_discount(100, 15) -> 85.0
    Raise ValueError if percent is below 0 or above 100.
    """
    raise NotImplementedError


def total_by_customer(invoices):
    """Sum invoice amounts per customer.

    invoices is a list of dicts like {"customer": "Acme", "amount": 100.0}
    Return a dict: {"Acme": 250.0, "Bluefin": 80.0}
    """
    raise NotImplementedError


def overdue_invoice_numbers(invoices, today):
    """Invoice numbers that are past due and still have a balance.

    invoices: list of dicts with "number", "due_date" (a datetime.date), "balance"
    today: a datetime.date
    Past due means due_date is before today. Return numbers in the original order.
    """
    raise NotImplementedError


def normalize_email(email):
    """Trim spaces and lowercase an email.

    normalize_email("  AP@Acme.COM ") -> "ap@acme.com"
    """
    raise NotImplementedError


def parse_plan_code(code):
    """Split a plan code like "PRO-ANNUAL-USD" into its parts.

    Return {"tier": "PRO", "term": "ANNUAL", "currency": "USD"}.
    Raise ValueError if the code does not have exactly 3 parts.
    """
    raise NotImplementedError


def total_mrr(subscriptions):
    """Monthly recurring revenue across subscriptions, rounded to 2 decimals.

    Each subscription: {"unit_price": 50.0, "quantity": 10, "period": "Month" or "Annual"}
    unit_price is per unit per billing period. Annual prices count as price / 12 per month.
    """
    raise NotImplementedError


def ramp_schedule(start_price, increase_percent, years):
    """Yearly prices for a ramp deal, each rounded to 2 decimals.

    ramp_schedule(1000, 10, 3) -> [1000.0, 1100.0, 1210.0]
    Each year is the previous year's price increased by increase_percent.
    """
    raise NotImplementedError


def top_customers(totals, n):
    """The n customers with the highest totals, highest first.

    totals: {"Acme": 250.0, "Bluefin": 80.0, "Cedar": 300.0}
    top_customers(totals, 2) -> ["Cedar", "Acme"]
    Hint: sorted(..., key=..., reverse=True)
    """
    raise NotImplementedError
