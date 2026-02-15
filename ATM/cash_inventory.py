from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DispenseContext:
    remaining: int
    available_notes: dict[int, int]
    dispensed: dict[int, int] = field(default_factory=dict)


class CashDispenser:
    def __init__(self, denomination: int) -> None:
        self.denomination = denomination
        self._next: Optional["CashDispenser"] = None

    def set_next(self, next_dispenser: "CashDispenser") -> "CashDispenser":
        self._next = next_dispenser
        return next_dispenser

    def handle(self, context: DispenseContext) -> None:
        available = context.available_notes.get(self.denomination, 0)
        use_count = min(context.remaining // self.denomination, available)
        if use_count > 0:
            context.dispensed[self.denomination] = use_count
            context.remaining -= self.denomination * use_count
            context.available_notes[self.denomination] -= use_count
        if self._next:
            self._next.handle(context)


class CashInventory:
    def __init__(self, notes: Optional[dict[int, int]] = None) -> None:
        self.notes = notes or {2000: 0, 500: 0, 200: 0, 100: 0}
        self._chain = self._build_chain()

    def _build_chain(self) -> CashDispenser:
        denominations = sorted(self.notes.keys(), reverse=True)
        if not denominations:
            raise ValueError("Cash inventory must contain denominations.")
        head = CashDispenser(denominations[0])
        current = head
        for denomination in denominations[1:]:
            current = current.set_next(CashDispenser(denomination))
        return head

    def total_amount(self) -> int:
        return sum(denomination * count for denomination, count in self.notes.items())

    def can_dispense(self, amount: int) -> bool:
        if amount <= 0 or amount % 100 != 0:
            return False
        return self._build_dispense_plan(amount) is not None

    def dispense(self, amount: int) -> dict[int, int]:
        plan = self._build_dispense_plan(amount)
        if plan is None:
            raise ValueError("ATM cannot dispense the requested amount.")
        for denomination, count in plan.items():
            self.notes[denomination] -= count
        return plan

    def accept_deposit(self, incoming_notes: dict[int, int]) -> int:
        amount = 0
        for denomination, count in incoming_notes.items():
            if denomination not in self.notes:
                raise ValueError(f"Unsupported denomination: {denomination}")
            if count < 0:
                raise ValueError("Note count cannot be negative.")
            self.notes[denomination] += count
            amount += denomination * count
        return amount

    def _build_dispense_plan(self, amount: int) -> Optional[dict[int, int]]:
        context = DispenseContext(remaining=amount, available_notes=self.notes.copy())
        self._chain.handle(context)
        if context.remaining == 0:
            return context.dispensed
        return None

