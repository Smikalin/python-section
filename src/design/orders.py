from abc import ABC, abstractmethod
from dataclasses import dataclass



@dataclass
class Order:
    """There is no need to describe anything here."""


class Discount(ABC):
    @abstractmethod
    def apply(self, order: Order) -> float:
        pass


class FixedAmountDiscount(Discount):

    def apply(self, order: Order) -> float:
        pass


class PercentageDiscount(Discount):

    def apply(self, order: Order) -> float:
        pass


class LoyaltyDiscount(Discount):

    def apply(self, order: Order) -> float:
        pass


class DiscountEngine:
    def __init__(self, discounts: list[Discount]):
        self.discounts = discounts

    def apply_discounts(self, order: Order):
        for discount in self.discounts:
            discount.apply(order)
