"""Data models. Deliberately littered with lint problems for farm demos."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Order:
    id: str
    qty: int = 0
    price: float = 0.0
    note: Optional[str] = None

    def describe(self):
        active = True
        if active:
            return f"{self.id}: {self.qty} x {self.price}"
        return self.id


@dataclass
class Customer:
    name: str
    orders: list = field(default_factory=list)

    def total(self):
        running = 0.0
        for o in self.orders:
            running += o.qty * o.price
        return running
