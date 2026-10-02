# Week 1, Saturday: Subscription billing calculator CLI

This is your first real build. Treat this file like a customer requirement.

## The ask

Sales ops wants a quick command-line tool to price a subscription before it goes into CPQ.

```
python billing_calc.py --unit-price 50 --quantity 100 --period annual --years 3 --ramp 7 --discount 10
```

Output:

```
Year  List price   Discount   Net price   Monthly equivalent
1     $60,000.00   $6,000.00  $54,000.00  $4,500.00
2     $64,200.00   $6,420.00  $57,780.00  $4,815.00
3     $68,694.00   $6,869.40  $61,824.60  $5,152.05
Total contract value (TCV): $173,604.60
```

## Rules

- `--unit-price` is per unit per **month**.
- `--period` is `monthly` or `annual`. It changes only the label on the invoice schedule line you print at the end ("Billed monthly: 12 invoices/year" or "Billed annually: 1 invoice/year").
- `--ramp` is the yearly price increase in percent (default 0). Use your `ramp_schedule` function.
- `--discount` is a percent (default 0). Use your `apply_discount` function, which rejects bad values.
- `--years` defaults to 1.
- Bad input (negative quantity, discount over 100) prints a clear error and exits with code 1. No stack traces.

## Steps

1. Read the [argparse tutorial](https://docs.python.org/3/howto/argparse.html) (20 minutes).
2. Create `billing_calc.py`. Parse the arguments and print them. Run it.
3. Import your functions from `exercises.py`. Compute year 1 only. Check the number by hand.
4. Add years and ramp. Check year 2 by hand.
5. Format the table with f-strings and `format_currency`.
6. Add error handling with `try/except ValueError` and `sys.exit(1)`.
7. Write 3 example commands in your repo README, with their output.

## Done when

The three scenarios below run and match your hand calculation, and they are in your README.

| Scenario | Command |
| --- | --- |
| Simple monthly | `--unit-price 25 --quantity 10 --period monthly` |
| 3-year ramp | the command at the top of this file |
| Bad input | `--unit-price 50 --quantity 10 --discount 150` → error, exit code 1 |

Sunday you'll write 5 pytest tests for it. Write the code so the math lives in a function (`price_contract(...)` returning a list of rows) separate from the printing; that makes testing easy.
