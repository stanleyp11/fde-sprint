from datetime import date

import pytest

from exercises import (
    annual_to_monthly,
    apply_discount,
    format_currency,
    normalize_email,
    overdue_invoice_numbers,
    parse_plan_code,
    ramp_schedule,
    top_customers,
    total_by_customer,
    total_mrr,
)


def test_format_currency():
    assert format_currency(1234.5) == "$1,234.50"
    assert format_currency(0) == "$0.00"
    assert format_currency(-20) == "-$20.00"


def test_annual_to_monthly():
    assert annual_to_monthly(1200) == 100.0
    assert annual_to_monthly(1000) == 83.33


def test_apply_discount():
    assert apply_discount(100, 15) == 85.0
    assert apply_discount(99.99, 0) == 99.99
    with pytest.raises(ValueError):
        apply_discount(100, 120)
    with pytest.raises(ValueError):
        apply_discount(100, -5)


def test_total_by_customer():
    rows = [
        {"customer": "Acme", "amount": 100.0},
        {"customer": "Bluefin", "amount": 80.0},
        {"customer": "Acme", "amount": 150.0},
    ]
    assert total_by_customer(rows) == {"Acme": 250.0, "Bluefin": 80.0}
    assert total_by_customer([]) == {}


def test_overdue_invoice_numbers():
    rows = [
        {"number": "INV1", "due_date": date(2026, 9, 1), "balance": 100.0},
        {"number": "INV2", "due_date": date(2026, 9, 1), "balance": 0.0},
        {"number": "INV3", "due_date": date(2026, 10, 30), "balance": 50.0},
        {"number": "INV4", "due_date": date(2026, 8, 15), "balance": 10.0},
    ]
    assert overdue_invoice_numbers(rows, date(2026, 10, 5)) == ["INV1", "INV4"]


def test_normalize_email():
    assert normalize_email("  AP@Acme.COM ") == "ap@acme.com"


def test_parse_plan_code():
    assert parse_plan_code("PRO-ANNUAL-USD") == {"tier": "PRO", "term": "ANNUAL", "currency": "USD"}
    with pytest.raises(ValueError):
        parse_plan_code("PRO-ANNUAL")


def test_total_mrr():
    subs = [
        {"unit_price": 50.0, "quantity": 10, "period": "Month"},
        {"unit_price": 1200.0, "quantity": 2, "period": "Annual"},
    ]
    assert total_mrr(subs) == 700.0


def test_ramp_schedule():
    assert ramp_schedule(1000, 10, 3) == [1000.0, 1100.0, 1210.0]
    assert ramp_schedule(500, 0, 2) == [500.0, 500.0]


def test_top_customers():
    totals = {"Acme": 250.0, "Bluefin": 80.0, "Cedar": 300.0}
    assert top_customers(totals, 2) == ["Cedar", "Acme"]
    assert top_customers(totals, 10) == ["Cedar", "Acme", "Bluefin"]
