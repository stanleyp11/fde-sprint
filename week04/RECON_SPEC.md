# Week 4 spec: Billing-to-payments reconciliation CLI

Write this like a deliverable for a client. Treat this file as the customer's requirement.

## Background (from the "customer")

> Our finance team closes the month by exporting Zuora invoices and Stripe charges into spreadsheets and matching them by hand. It takes two people three days, and we still miss duplicate charges. We want a tool that runs in minutes and gives us a clean exceptions list.

## What it must do

1. Read invoices and charges from either the CSVs in `data/` **or** Postgres (`--source csv|db`).
2. Match each Stripe charge to an invoice using `metadata_invoice_number`.
3. Report every exception in one of five categories:

| Category | Rule |
| --- | --- |
| `MISSING_PAYMENT` | Invoice has no charge at all |
| `FAILED_PAYMENT` | Invoice has charges, but none succeeded |
| `DUPLICATE_CHARGE` | More than one successful charge for one invoice |
| `AMOUNT_MISMATCH` | One successful charge, but its amount differs from the invoice by more than $0.01 |
| `ORPHAN_CHARGE` | Successful charge with no invoice number, or a number that matches no invoice |

4. Print a summary table to the console and write `exceptions.csv` with columns `category, reference, invoiced, collected, difference`.
5. Exit code 0 when there are no exceptions, 2 when there are. (Finance will run it in a scheduled job later.)

## Interface you must implement

`week04/recon/matcher.py` exposes:

```python
def reconcile(invoices: list[dict], charges: list[dict]) -> list[Exception_]:
    ...
```

`invoices` rows have `invoiceNumber` and `amount` (dollars). `charges` rows have `id`, `amount_cents`, `status`, `metadata_invoice_number`. Return a list of `Exception_` dataclass objects with fields `category`, `reference`, `invoiced`, `collected`, sorted by category then reference. (The trailing underscore avoids shadowing Python's built-in `Exception`.)

`pytest week04/tests -v` checks your matcher. These are acceptance tests: you write the code to make them pass and don't change the tests.

## Day by day

| Day | Do |
| --- | --- |
| Mon | Write the README "Design" section: inputs, matching rules, outputs, edge cases. No code. |
| Tue | Implement `matcher.py` until `pytest week04/tests` passes. |
| Wed | `report.py`: console table with [rich](https://rich.readthedocs.io/en/stable/tables.html) + `exceptions.csv`. |
| Thu | `--source zuora`: pull invoices from the mock Zuora API (`MOCK_FAIL_RATE=0.3`) with retries on 429. Add `--source db`. |
| Fri | Code-reading drill (see the study guide). |
| Sat | README, diagram, Loom, tag `v1.0`. |
| Sun | LinkedIn post and month retro. |

## Done when

- `python -m week04.recon --source csv` prints the 5 planted exceptions and exits with code 2.
- `pytest week04/tests` passes.
- Someone who has never seen your repo can run it in under 5 minutes from your README.
