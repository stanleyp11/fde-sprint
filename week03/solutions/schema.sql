-- Reference schema. Design your own first (Tuesday), then compare.
DROP TABLE IF EXISTS stripe_charges, invoices, subscriptions, accounts CASCADE;

CREATE TABLE accounts (
    id                 text PRIMARY KEY,
    account_number     text UNIQUE NOT NULL,
    name               text NOT NULL,
    currency           char(3) NOT NULL,
    bill_to_email      text,
    stripe_customer_id text UNIQUE,
    status             text NOT NULL
);

CREATE TABLE subscriptions (
    id                  text PRIMARY KEY,
    subscription_number text UNIQUE NOT NULL,
    account_number      text NOT NULL REFERENCES accounts(account_number),
    status              text NOT NULL,
    product_name        text NOT NULL,
    rate_plan_name      text NOT NULL,
    quantity            integer NOT NULL CHECK (quantity > 0),
    list_price_per_unit numeric(12,2) NOT NULL,
    discount_percent    numeric(5,2) NOT NULL DEFAULT 0,
    billing_period      text NOT NULL CHECK (billing_period IN ('Month','Annual')),
    term_start_date     date NOT NULL,
    term_end_date       date NOT NULL,
    mrr                 numeric(12,2) NOT NULL
);

CREATE TABLE invoices (
    id             text PRIMARY KEY,
    invoice_number text UNIQUE NOT NULL,
    account_number text NOT NULL REFERENCES accounts(account_number),
    invoice_date   date NOT NULL,
    due_date       date NOT NULL,
    amount         numeric(12,2) NOT NULL,
    balance        numeric(12,2) NOT NULL,
    currency       char(3) NOT NULL,
    status         text NOT NULL
);

CREATE TABLE stripe_charges (
    id                      text PRIMARY KEY,
    customer                text NOT NULL,
    amount_cents            integer NOT NULL,
    currency                char(3) NOT NULL,
    created                 date NOT NULL,
    status                  text NOT NULL,
    description             text,
    metadata_invoice_number text
);

CREATE INDEX ON invoices (account_number);
CREATE INDEX ON stripe_charges (metadata_invoice_number);
