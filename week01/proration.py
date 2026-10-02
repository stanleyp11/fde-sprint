"""Week 1, Wednesday: proration, the way billing systems do it.

A customer pays `amount` for a service period. Partway through, they change
plan. Prorate = the share of `amount` for the days left in the period.

Convention (same as Zuora's default day-based proration):
  - period_end is EXCLUSIVE (it is the next bill date)
  - days_in_period = (period_end - period_start).days
  - days_remaining = (period_end - change_date).days
  - result = amount * days_remaining / days_in_period, rounded to 2 decimals

Raise ValueError if change_date is outside [period_start, period_end).

Run:  pytest week01/tests/test_proration.py -v
Then check 3 cases by hand on paper and write them in your notes.
"""
from datetime import date


def prorate(amount: float, period_start: date, period_end: date, change_date: date) -> float:
    raise NotImplementedError
