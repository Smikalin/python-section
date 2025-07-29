
from src.wallets.exceptions import (
    NegativeValueException,
    NotComparisonException,
)


class Money:
    def __init__(self, value, currency):
        if value < 0:
            raise NegativeValueException(
                "Значение не может быть отрицательным"
            )
        self.value = value
        self.currency = currency

    def __add__(self, other):
        """
        Складывает деньги.
        Если валюты не совпадают, то выбрасывается
        исключение NotComparisonException.
        """
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise NotComparisonException(
                "Невозможно сложить деньги с разными валютами"
            )
        return Money(self.value + other.value, self.currency)

    def __sub__(self, other):
        """
        Вычитает деньги.
        Если валюты не совпадают, то выбрасывается исключение
        NotComparisonException.
        Если результат меньше 0, то выбрасывается исключение
        NegativeValueException.
        """
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise NotComparisonException(
                "Невозможно вычесть деньги с разными валютами"
            )
        result = self.value - other.value
        if result < 0:
            raise NegativeValueException(
                "Результат не может быть отрицательным"
            )
        return Money(result, self.currency)

    def __eq__(self, other):
        """
        Проверяет, равны ли деньги.
        """
        if not isinstance(other, Money):
            return False
        return self.value == other.value and self.currency == other.currency

    def __repr__(self):
        """
        Возвращает строковое представление денег.
        """
        return f"Money(value={self.value}, currency={self.currency})"


class Wallet:
    def __init__(self, money: Money):
        self.currencies = {}
        if money.value > 0:
            self.currencies[money.currency] = money

    def __getitem__(self, currency):
        """
        Возвращает деньги в указанной валюте.
        Если в кошельке нет денег в этой валюте, то возвращается 0.
        """
        if currency in self.currencies:
            return self.currencies[currency]
        return Money(0, currency)

    def __delitem__(self, currency):
        """
        Удаляет деньги в указанной валюте из кошелька.
        """
        if currency in self.currencies:
            del self.currencies[currency]

    def __contains__(self, currency):
        """
        Проверяет, есть ли деньги в указанной валюте в кошельке.
        """
        return currency in self.currencies

    def __len__(self):
        """
        Возвращает количество валют в кошельке.
        """
        return len(self.currencies)

    def add(self, money: Money):
        """
        Добавляет деньги в кошелек.
        Если в кошельке уже есть деньги в этой валюте, то суммирует их.
        """
        if money.currency in self.currencies:
            self.currencies[money.currency] = (
                self.currencies[money.currency] + money
            )
        else:
            self.currencies[money.currency] = money
        return self

    def sub(self, money: Money):
        """
        Изымает деньги из кошелька.
        Если сумма денег в кошельке меньше суммы, которую нужно изымать,
        то выбрасывается исключение NegativeValueException.
        """
        if money.currency in self.currencies:
            self.currencies[money.currency] = (
                self.currencies[money.currency] - money
            )
            if self.currencies[money.currency].value == 0:
                del self.currencies[money.currency]
        else:
            if money.value > 0:
                raise NegativeValueException(
                    "Недостаточно денег для вычитания"
                )
        return self
