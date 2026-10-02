"""Your reconciliation logic lives here. See week04/RECON_SPEC.md.

Suggested approach (pseudo-code, not Python):
  1. index invoices by invoiceNumber
  2. group charges by metadata_invoice_number
  3. charges whose number is empty or not in the index -> ORPHAN_CHARGE (successful ones only)
  4. for each invoice:
       no charges                       -> MISSING_PAYMENT
       charges but none succeeded       -> FAILED_PAYMENT
       more than one succeeded          -> DUPLICATE_CHARGE
       one succeeded, amount off > 0.01 -> AMOUNT_MISMATCH
  5. sort by (category, reference)

Work in cents (integers) internally to avoid floating-point surprises:
  round(invoice["amount"] * 100)
"""
from dataclasses import dataclass


@dataclass
class Exception_:
    category: str
    reference: str
    invoiced: float | None
    collected: float


def reconcile(invoices: list[dict], charges: list[dict]) -> list[Exception_]:
    raise NotImplementedError
