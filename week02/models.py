"""Week 2, Monday: model your billing objects with dataclasses.

Fill in the four classes, then make  pytest week02/tests -v  pass.
Learn: https://docs.python.org/3/library/dataclasses.html (first 3 sections)
"""
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Account:
    account_number: str
    name: str
    currency: str = "USD"
    # TODO: add bill_to_email: str = ""


@dataclass
class Subscription:
    subscription_number: str
    account_number: str
    unit_price: float      # per unit per billing period
    quantity: int
    billing_period: str    # "Month" or "Annual"
    discount_percent: float = 0.0

    def mrr(self) -> float:
        """Monthly recurring revenue after discount, rounded to 2 decimals."""
        # TODO: annual prices count as /12. Apply the discount.
        raise NotImplementedError


@dataclass
class Invoice:
    invoice_number: str
    account_number: str
    invoice_date: date
    due_date: date
    amount: float
    balance: float = 0.0

    def is_overdue(self, today: date) -> bool:
        # TODO: past due date with balance above 0
        raise NotImplementedError


@dataclass
class Payment:
    payment_id: str
    invoice_number: str
    amount: float
    status: str = "succeeded"
    tags: list[str] = field(default_factory=list)
