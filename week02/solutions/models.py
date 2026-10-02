"""Reference solution for week02/models.py."""
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Account:
    account_number: str
    name: str
    currency: str = "USD"
    bill_to_email: str = ""


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
        per_period = self.unit_price * self.quantity * (1 - self.discount_percent / 100)
        return round(per_period / 12 if self.billing_period == "Annual" else per_period, 2)


@dataclass
class Invoice:
    invoice_number: str
    account_number: str
    invoice_date: date
    due_date: date
    amount: float
    balance: float = 0.0

    def is_overdue(self, today: date) -> bool:
        return self.due_date < today and self.balance > 0


@dataclass
class Payment:
    payment_id: str
    invoice_number: str
    amount: float
    status: str = "succeeded"
    tags: list[str] = field(default_factory=list)
