import enum
from dataclasses import dataclass


class AvailableCurrencies(enum.Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


@dataclass
class Currency:
    name: AvailableCurrencies
    symbol: str
    precision: int


@dataclass
class RUB(Currency):
    def __init__(self):
        self.name = AvailableCurrencies.RUB
        self.symbol = "₽"
        self.precision = 2


@dataclass
class USD(Currency):
    def __init__(self):
        self.name = AvailableCurrencies.USD
        self.symbol = "$"
        self.precision = 2


rub = RUB()
usd = USD()
