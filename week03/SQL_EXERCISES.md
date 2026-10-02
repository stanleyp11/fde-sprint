# Week 3 SQL exercises

Run these against your `o2c` database after Friday's load (or load with the reference script first: `python week03/solutions/load_data.py`).

Open a SQL prompt: `docker compose -f week03/docker-compose.yml exec db psql -U fde -d o2c`
Or use a GUI: [DBeaver](https://dbeaver.io/) (free) or [TablePlus](https://tableplus.com/).

Write each answer in `week03/my_answers.sql`. Check against `week03/solutions/answers.sql` only after trying.

## Level 1 — Tuesday (SELECT, WHERE, ORDER BY, GROUP BY)

1. List all accounts alphabetically (account number, name).
2. Subscriptions with quantity of 100 or more, largest first.
3. Number of subscriptions per rate plan.
4. Total invoiced amount per account, top 5.
5. Total MRR, then MRR split by billing period.

## Level 2 — Wednesday (JOINs)

6. The first 10 invoices by date, with the account name next to each.
7. Open invoices (balance above 0) with customer name and days overdue as of 2026-10-05.
8. Accounts with no open balance at all. Try it two ways: `LEFT JOIN ... IS NULL` and `NOT EXISTS`.
9. Each invoice with the dollars actually collected in Stripe. Remember Stripe stores **cents**.

## Level 3 — Thursday (dates and window functions)

10. Invoiced amount by month.
11. Running total of invoiced amount per account, by date. Learn: [Postgres window functions tutorial](https://www.postgresql.org/docs/current/tutorial-window.html).
12. Rank accounts by total invoiced.
13. Month-over-month change in invoiced amount (use `LAG`).
14. Stripe customers with charges but no matching Zuora account.

## Level 4 — Saturday (the real thing)

15. **Reconciliation.** One query that lists every problem between Zuora invoices and Stripe charges, one row per issue, with a category: missing payment, failed payment, duplicate charge, amount mismatch, orphan charge.

The dataset has exactly **5 planted issues**. You're done when your query finds all 5 and nothing else. The answer key is in `data/PLANTED_ISSUES.md`; don't open it until you think you've found them all.
