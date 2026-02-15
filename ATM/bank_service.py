from .models import BankAccount, Card


class BankService:
    def __init__(self) -> None:
        self._accounts: dict[str, BankAccount] = {}
        self._cards: dict[str, Card] = {}

    def add_account(self, account: BankAccount) -> None:
        self._accounts[account.account_number] = account

    def add_card(self, card: Card) -> None:
        self._cards[card.card_number] = card

    def has_card(self, card_number: str) -> bool:
        return card_number in self._cards

    def authenticate(self, card_number: str, pin: str) -> BankAccount:
        card = self._cards.get(card_number)
        if card is None or not card.is_active:
            raise ValueError("Invalid or inactive card.")
        if not card.validate_pin(pin):
            raise ValueError("Incorrect PIN.")
        account = self._accounts.get(card.account_number)
        if account is None:
            raise ValueError("Linked account not found.")
        return account

