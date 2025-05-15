from decimal import Decimal
import json


class WithdrawalEvent:
    def __init__(self, amount: Decimal, account_id: int, status: str):
        self.amount = amount
        self.account_id = account_id
        self.status = status

    def to_json(self):
        return json.dumps({"amount": str(self.amount), "account_id": self.account_id, "status": self.status})
