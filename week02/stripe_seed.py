"""Week 2, Friday: create Stripe test-mode data from Python.

Setup:
  1. Create a free account at https://dashboard.stripe.com/register (no business details needed for test mode).
  2. Make sure the dashboard toggle says "Test mode".
  3. Copy the secret key (sk_test_...) into STRIPE_API_KEY in .env.
  4. pip install stripe python-dotenv

Run:  python week02/stripe_seed.py
Done when: 5 customers and 2 prices appear in the Stripe dashboard (test mode).

This file uses the official stripe library. Steps are TODOs; docs:
  https://docs.stripe.com/api/customers/create
  https://docs.stripe.com/api/products/create
  https://docs.stripe.com/api/prices/create
"""
import csv
import os

import stripe
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.environ["STRIPE_API_KEY"]
assert stripe.api_key.startswith("sk_test_"), "Use a TEST key only (sk_test_...)."


def main():
    # TODO 1: read the first 5 rows of data/accounts.csv
    # TODO 2: for each, stripe.Customer.create(name=..., email=..., metadata={"zuora_account": accountNumber})
    #         print the new customer id
    # TODO 3: create one Product named "Platform"
    # TODO 4: create two Prices for it: 6000 cents monthly, 60000 cents yearly
    #         (unit_amount=..., currency="usd", recurring={"interval": "month"} or "year")
    # TODO 5: make it safe to re-run: search for an existing customer by email first
    #         (stripe.Customer.list(email=...)) and skip it if found
    raise NotImplementedError


if __name__ == "__main__":
    main()
