from __future__ import annotations

from typing import Optional

from .bank_service import BankService
from .cash_inventory import CashInventory
from .enums import TransactionType
from .models import BankAccount
from .states import ATMState, IdleState
from .transactions import TransactionProcessor, default_processors


class ATM:
    def __init__(self, atm_id: str, bank_service: BankService, cash_inventory: CashInventory) -> None:
        self.atm_id = atm_id
        self.bank_service = bank_service
        self.cash_inventory = cash_inventory
        self.state: ATMState = IdleState()
        self.current_card_number: Optional[str] = None
        self.current_account: Optional[BankAccount] = None
        self.transaction_processors: dict[TransactionType, TransactionProcessor] = default_processors()

    def set_state(self, state: ATMState) -> None:
        self.state = state

    def reset_session(self) -> None:
        self.current_card_number = None
        self.current_account = None

    def insert_card(self, card_number: str) -> str:
        return self.state.insert_card(self, card_number)

    def authenticate(self, pin: str) -> str:
        return self.state.authenticate(self, pin)

    def perform_transaction(
        self,
        txn_type: TransactionType,
        amount: int = 0,
        deposit_notes: Optional[dict[int, int]] = None,
    ) -> str:
        return self.state.perform_transaction(self, txn_type, amount, deposit_notes)

    def eject_card(self) -> str:
        return self.state.eject_card(self)

