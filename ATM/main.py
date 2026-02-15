from __future__ import annotations

import os
import sys

if __package__ is None or __package__ == "":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

from ATM.atm_machine import ATM
from ATM.bank_service import BankService
from ATM.cash_inventory import CashInventory
from ATM.enums import TransactionType
from ATM.models import BankAccount, Card


def build_demo_atm() -> ATM:
    bank_service = BankService()
    account = BankAccount(account_number="ACC-1001", holder_name="Alice", balance=10000)
    card = Card(card_number="CARD-1111", pin="1234", account_number="ACC-1001")
    bank_service.add_account(account)
    bank_service.add_card(card)

    inventory = CashInventory({2000: 4, 500: 10, 200: 10, 100: 20})
    return ATM(atm_id="ATM-01", bank_service=bank_service, cash_inventory=inventory)


def main() -> None:
    atm = build_demo_atm()
    print("=== ATM LLD Demo ===")
    print(atm.insert_card("CARD-1111"))
    print(atm.authenticate("1234"))
    print(atm.perform_transaction(TransactionType.BALANCE))
    print(atm.perform_transaction(TransactionType.WITHDRAW, amount=2700))
    print(atm.perform_transaction(TransactionType.DEPOSIT, deposit_notes={500: 2, 100: 5}))
    print(atm.perform_transaction(TransactionType.BALANCE))
    print(atm.eject_card())
    print(f"ATM cash left: {atm.cash_inventory.total_amount()}")


if __name__ == "__main__":
    main()

