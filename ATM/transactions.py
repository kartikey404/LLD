from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

from .enums import TransactionType

if TYPE_CHECKING:
    from .atm_machine import ATM


class TransactionProcessor(ABC):
    @abstractmethod
    def execute(self, atm: "ATM", amount: int = 0, deposit_notes: Optional[dict[int, int]] = None) -> str:
        raise NotImplementedError


class BalanceInquiryProcessor(TransactionProcessor):
    def execute(self, atm: "ATM", amount: int = 0, deposit_notes: Optional[dict[int, int]] = None) -> str:
        if atm.current_account is None:
            raise ValueError("No authenticated account.")
        return f"Available balance: {atm.current_account.balance}"


class WithdrawProcessor(TransactionProcessor):
    def execute(self, atm: "ATM", amount: int = 0, deposit_notes: Optional[dict[int, int]] = None) -> str:
        if atm.current_account is None:
            raise ValueError("No authenticated account.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if not atm.cash_inventory.can_dispense(amount):
            raise ValueError("ATM cannot dispense this amount with current cash.")
        atm.current_account.debit(amount)
        dispensed = atm.cash_inventory.dispense(amount)
        return f"Withdraw success: {amount}, notes={dispensed}"


class DepositProcessor(TransactionProcessor):
    def execute(self, atm: "ATM", amount: int = 0, deposit_notes: Optional[dict[int, int]] = None) -> str:
        if atm.current_account is None:
            raise ValueError("No authenticated account.")
        if not deposit_notes:
            raise ValueError("Deposit notes required.")
        total = atm.cash_inventory.accept_deposit(deposit_notes)
        atm.current_account.credit(total)
        return f"Deposit success: {total}"


def default_processors() -> dict[TransactionType, TransactionProcessor]:
    return {
        TransactionType.BALANCE: BalanceInquiryProcessor(),
        TransactionType.WITHDRAW: WithdrawProcessor(),
        TransactionType.DEPOSIT: DepositProcessor(),
    }

