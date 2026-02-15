from __future__ import annotations

from abc import ABC
from typing import Optional, TYPE_CHECKING

from .enums import TransactionType

if TYPE_CHECKING:
    from .atm_machine import ATM


class ATMState(ABC):
    def insert_card(self, atm: "ATM", card_number: str) -> str:
        raise ValueError("Invalid operation in current state.")

    def authenticate(self, atm: "ATM", pin: str) -> str:
        raise ValueError("Invalid operation in current state.")

    def perform_transaction(
        self,
        atm: "ATM",
        txn_type: TransactionType,
        amount: int = 0,
        deposit_notes: Optional[dict[int, int]] = None,
    ) -> str:
        raise ValueError("Invalid operation in current state.")

    def eject_card(self, atm: "ATM") -> str:
        raise ValueError("Invalid operation in current state.")


class IdleState(ATMState):
    def insert_card(self, atm: "ATM", card_number: str) -> str:
        if not atm.bank_service.has_card(card_number):
            raise ValueError("Card not recognized.")
        atm.current_card_number = card_number
        atm.set_state(CardInsertedState())
        return "Card inserted. Please enter PIN."


class CardInsertedState(ATMState):
    def authenticate(self, atm: "ATM", pin: str) -> str:
        if atm.current_card_number is None:
            raise ValueError("No card present.")
        account = atm.bank_service.authenticate(atm.current_card_number, pin)
        atm.current_account = account
        atm.set_state(AuthenticatedState())
        return f"Authentication successful. Welcome {account.holder_name}."

    def eject_card(self, atm: "ATM") -> str:
        atm.reset_session()
        atm.set_state(IdleState())
        return "Card ejected."


class AuthenticatedState(ATMState):
    def perform_transaction(
        self,
        atm: "ATM",
        txn_type: TransactionType,
        amount: int = 0,
        deposit_notes: Optional[dict[int, int]] = None,
    ) -> str:
        processor = atm.transaction_processors[txn_type]
        return processor.execute(atm, amount=amount, deposit_notes=deposit_notes)

    def eject_card(self, atm: "ATM") -> str:
        atm.reset_session()
        atm.set_state(IdleState())
        return "Session ended. Card ejected."

