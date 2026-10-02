-- Answer key for week03/SQL_EXERCISES.md. Try each one yourself first.

-- 1. All accounts, alphabetical
SELECT account_number, name FROM accounts ORDER BY name;

-- 2. Subscriptions with quantity of 100 or more
SELECT subscription_number, account_number, quantity FROM subscriptions WHERE quantity >= 100 ORDER BY quantity DESC;

-- 3. Number of subscriptions per rate plan
SELECT rate_plan_name, count(*) AS subs FROM subscriptions GROUP BY rate_plan_name ORDER BY subs DESC;

-- 4. Total invoiced amount per account, top 5
SELECT account_number, sum(amount) AS invoiced FROM invoices GROUP BY account_number ORDER BY invoiced DESC LIMIT 5;

-- 5. Total MRR, and MRR by billing period
SELECT sum(mrr) AS total_mrr FROM subscriptions;
SELECT billing_period, sum(mrr) AS mrr FROM subscriptions GROUP BY billing_period;

-- 6. Invoices with the account name (JOIN)
SELECT i.invoice_number, a.name, i.invoice_date, i.amount
FROM invoices i JOIN accounts a ON a.account_number = i.account_number
ORDER BY i.invoice_date LIMIT 10;

-- 7. Open invoices (balance > 0) with customer name and days overdue as of 2026-10-05
SELECT i.invoice_number, a.name, i.balance, DATE '2026-10-05' - i.due_date AS days_overdue
FROM invoices i JOIN accounts a ON a.account_number = i.account_number
WHERE i.balance > 0 ORDER BY days_overdue DESC;

-- 8. Accounts with no open balance at all (LEFT JOIN or NOT EXISTS)
SELECT a.name FROM accounts a
WHERE NOT EXISTS (SELECT 1 FROM invoices i WHERE i.account_number = a.account_number AND i.balance > 0)
ORDER BY a.name;

-- 9. Each invoice with its successful Stripe payment total (LEFT JOIN, cents to dollars)
SELECT i.invoice_number, i.amount,
       coalesce(sum(c.amount_cents) FILTER (WHERE c.status = 'succeeded'), 0) / 100.0 AS paid
FROM invoices i LEFT JOIN stripe_charges c ON c.metadata_invoice_number = i.invoice_number
GROUP BY i.invoice_number, i.amount ORDER BY i.invoice_number LIMIT 10;

-- 10. Invoiced amount by month (2026)
SELECT to_char(invoice_date, 'YYYY-MM') AS month, sum(amount) AS invoiced
FROM invoices GROUP BY 1 ORDER BY 1;

-- 11. Running total of invoiced amount per account (window function)
SELECT account_number, invoice_date, amount,
       sum(amount) OVER (PARTITION BY account_number ORDER BY invoice_date) AS running_total
FROM invoices ORDER BY account_number, invoice_date LIMIT 15;

-- 12. Rank accounts by total invoiced (window function)
SELECT account_number, invoiced, rank() OVER (ORDER BY invoiced DESC) AS rnk
FROM (SELECT account_number, sum(amount) AS invoiced FROM invoices GROUP BY account_number) t;

-- 13. Month-over-month change in invoiced amount (LAG)
WITH m AS (SELECT to_char(invoice_date, 'YYYY-MM') AS month, sum(amount) AS invoiced FROM invoices GROUP BY 1)
SELECT month, invoiced, invoiced - lag(invoiced) OVER (ORDER BY month) AS change FROM m ORDER BY month;

-- 14. Customers whose Stripe customer id has charges but no matching Zuora account
SELECT DISTINCT c.customer FROM stripe_charges c
LEFT JOIN accounts a ON a.stripe_customer_id = c.customer WHERE a.id IS NULL;

-- 15. THE RECONCILIATION: every problem between invoices and Stripe, one row per issue
WITH paid AS (
    SELECT metadata_invoice_number AS invoice_number,
           sum(amount_cents) FILTER (WHERE status = 'succeeded') AS ok_cents,
           count(*) FILTER (WHERE status = 'succeeded') AS ok_count,
           count(*) FILTER (WHERE status <> 'succeeded') AS failed_count
    FROM stripe_charges WHERE metadata_invoice_number <> '' GROUP BY 1
)
SELECT i.invoice_number AS ref,
       CASE
         WHEN p.invoice_number IS NULL THEN 'MISSING_PAYMENT'
         WHEN p.ok_count = 0 AND p.failed_count > 0 THEN 'FAILED_PAYMENT'
         WHEN p.ok_count > 1 THEN 'DUPLICATE_CHARGE'
         WHEN p.ok_cents <> round(i.amount * 100) THEN 'AMOUNT_MISMATCH'
       END AS issue,
       i.amount AS invoiced, (coalesce(p.ok_cents, 0) / 100.0)::numeric(12,2) AS collected
FROM invoices i LEFT JOIN paid p ON p.invoice_number = i.invoice_number
WHERE p.invoice_number IS NULL OR p.ok_count <> 1 OR p.ok_cents <> round(i.amount * 100)
UNION ALL
SELECT c.id, 'ORPHAN_CHARGE', NULL, (c.amount_cents / 100.0)::numeric(12,2)
FROM stripe_charges c
WHERE coalesce(c.metadata_invoice_number, '') = ''
   OR c.metadata_invoice_number NOT IN (SELECT invoice_number FROM invoices)
ORDER BY issue, ref;
