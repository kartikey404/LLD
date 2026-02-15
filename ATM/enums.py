from enum import Enum


class TransactionType(str, Enum):
    BALANCE = "BALANCE"
    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"

