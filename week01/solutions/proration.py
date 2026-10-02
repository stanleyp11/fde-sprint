from datetime import date


def prorate(amount: float, period_start: date, period_end: date, change_date: date) -> float:
    if not (period_start <= change_date < period_end):
        raise ValueError(f"change date {change_date} is outside {period_start}..{period_end}")
    days_in_period = (period_end - period_start).days
    days_remaining = (period_end - change_date).days
    return round(amount * days_remaining / days_in_period, 2)
