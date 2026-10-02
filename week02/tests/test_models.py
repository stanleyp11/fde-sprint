import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models import Account, Invoice, Subscription  # noqa: E402


def test_account_has_email():
    a = Account("A1", "Acme", bill_to_email="ap@acme.example.com")
    assert a.bill_to_email == "ap@acme.example.com"


def test_monthly_mrr_with_discount():
    s = Subscription("S1", "A1", unit_price=60.0, quantity=10, billing_period="Month", discount_percent=15)
    assert s.mrr() == 510.0


def test_annual_mrr():
    s = Subscription("S2", "A1", unit_price=1200.0, quantity=5, billing_period="Annual")
    assert s.mrr() == 500.0


def test_overdue():
    inv = Invoice("INV1", "A1", date(2026, 9, 1), date(2026, 10, 1), 100.0, balance=100.0)
    assert inv.is_overdue(date(2026, 10, 12))
    assert not inv.is_overdue(date(2026, 9, 15))
    paid = Invoice("INV2", "A1", date(2026, 9, 1), date(2026, 10, 1), 100.0, balance=0.0)
    assert not paid.is_overdue(date(2026, 10, 12))
