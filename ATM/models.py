from dataclasses import dataclass


@dataclass
class Card:
    card_number: str
    pin: str
    account_number: str
    is_active: bool = True

    def validate_pin(self, entered_pin: str) -> bool:
        return self.pin == entered_pin


@dataclass
class BankAccount:
    account_number: str
    holder_name: str
    balance: int

    def credit(self, amount: int) -> None:
        self.balance += amount

    def debit(self, amount: int) -> None:
        if amount > self.balance:
            raise ValueError("Insufficient account balance.")
        self.balance -= amount

