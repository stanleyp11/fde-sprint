# FDE Sprint starter pack (Month 1)

Materials for Weeks 1–4 of your sprint. Pair it with the **FDE Sprint Study Guide** (what to learn each day) and the **FDE Sprint Tracker** (tick off each day).

All data is synthetic. Never add real client data to this repo.

## Set up (Monday, Oct 5)

```bash
# inside your cloned fde-sprint repo, after unzipping this pack into it
python3.12 -m venv .venv           # macOS: use python3 / python3.12 until the venv is active
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env               # fill in keys as each week needs them
pytest week01/tests -q             # expect 14 failed: that's your Week 1 work
```

## What's inside

| Path | Week | What it is |
| --- | --- | --- |
| `week01/exercises.py` | 1 | 10 billing-flavored Python functions to write; tests check them |
| `week01/proration.py` | 1 | Day-based proration, Zuora style |
| `week01/invoice_totals.py` + `data/invoices_small.csv` | 1 | CSV reading with 2 broken rows on purpose |
| `week01/SATURDAY_billing_calculator.md` | 1 | Spec for your first CLI build |
| `week02/models.py` | 2 | Dataclasses for Account, Subscription, Invoice, Payment |
| `week02/http_drills.py` | 2 | 5 HTTP drills against the mock Zuora API |
| `week02/mock_zuora/server.py` | 2–4 | Mock Zuora API: OAuth, Object Query pagination, simulated 429s |
| `week02/stripe_seed.py`, `zuora_pull.py`, `sf_query.py` | 2 | Guided scripts with TODOs for each system |
| `week03/docker-compose.yml` | 3 | Postgres 16 in Docker |
| `week03/SQL_EXERCISES.md` | 3 | 15 SQL exercises, ending with the full reconciliation |
| `week03/load_data.py` | 3 | Idempotent CSV-to-Postgres loader (TODOs) |
| `week04/RECON_SPEC.md` | 4 | Client-style spec for Ship #1 |
| `week04/tests/test_matcher.py` | 4 | Acceptance tests your reconciliation must pass |
| `data/` | all | Synthetic Zuora accounts, subscriptions, invoices and Stripe charges with 5 planted issues |
| `tools/make_data.py` | all | Rebuilds `data/` |
| `templates/` | all | README template for your projects, weekly retro template |

## How to check your work

```bash
pytest week01/tests -v                       # your code
CHECK_SOLUTIONS=1 pytest week01/tests -q     # the reference solutions (should all pass)
```

Reference solutions are in each week's `solutions/` folder. Try for 20 minutes before looking. Week 4 has no solution: it's your ship.

## Mock Zuora API

```bash
uvicorn week02.mock_zuora.server:app --port 8040 --reload
# docs: http://localhost:8040/docs   credentials: demo-client / demo-secret
MOCK_FAIL_RATE=0.3 uvicorn week02.mock_zuora.server:app --port 8040   # practice retries
```
