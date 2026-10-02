"""Acceptance tests for week04/recon/matcher.py. Make these pass; don't edit them."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from week04.recon.matcher import reconcile  # noqa: E402


def inv(num, amount):
    return {"invoiceNumber": num, "amount": amount}


def ch(cid, num, cents, status="succeeded"):
    return {"id": cid, "metadata_invoice_number": num, "amount_cents": cents, "status": status}


def kinds(result):
    return [(e.category, e.reference) for e in result]


def test_clean_match_has_no_exceptions():
    assert reconcile([inv("I1", 100.0)], [ch("c1", "I1", 10000)]) == []


def test_missing_payment():
    assert kinds(reconcile([inv("I1", 100.0)], [])) == [("MISSING_PAYMENT", "I1")]


def test_failed_payment():
    r = reconcile([inv("I1", 100.0)], [ch("c1", "I1", 10000, "failed")])
    assert kinds(r) == [("FAILED_PAYMENT", "I1")]


def test_duplicate_charge():
    r = reconcile([inv("I1", 100.0)], [ch("c1", "I1", 10000), ch("c2", "I1", 10000)])
    assert kinds(r) == [("DUPLICATE_CHARGE", "I1")]
    assert r[0].collected == 200.0


def test_amount_mismatch_and_tolerance():
    r = reconcile([inv("I1", 100.0), inv("I2", 50.0)], [ch("c1", "I1", 9000), ch("c2", "I2", 5000)])
    assert kinds(r) == [("AMOUNT_MISMATCH", "I1")]
    assert r[0].invoiced == 100.0 and r[0].collected == 90.0


def test_failed_then_retried_successfully_is_clean():
    r = reconcile([inv("I1", 100.0)], [ch("c1", "I1", 10000, "failed"), ch("c2", "I1", 10000)])
    assert r == []


def test_orphan_charges():
    r = reconcile([inv("I1", 100.0)], [ch("c1", "I1", 10000), ch("c9", "", 4999), ch("c8", "NOPE", 100)])
    assert kinds(r) == [("ORPHAN_CHARGE", "c8"), ("ORPHAN_CHARGE", "c9")]


def test_sorted_by_category_then_reference():
    r = reconcile([inv("I2", 10.0), inv("I1", 10.0)], [ch("c9", "", 1)])
    assert kinds(r) == [("MISSING_PAYMENT", "I1"), ("MISSING_PAYMENT", "I2"), ("ORPHAN_CHARGE", "c9")]


def _load(name):
    with open(ROOT / "data" / name, newline="") as f:
        return list(csv.DictReader(f))


def test_full_dataset_finds_exactly_the_five_planted_issues():
    invoices = [{**r, "amount": float(r["amount"])} for r in _load("invoices.csv")]
    charges = [{**r, "amount_cents": int(r["amount_cents"])} for r in _load("stripe_charges.csv")]
    result = reconcile(invoices, charges)
    assert sorted(e.category for e in result) == [
        "AMOUNT_MISMATCH", "DUPLICATE_CHARGE", "FAILED_PAYMENT", "MISSING_PAYMENT", "ORPHAN_CHARGE"]
