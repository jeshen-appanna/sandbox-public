from decimal import Decimal
import json


class WithdrawalEvent:
    def __init__(self, account_id: int, amount: Decimal, status: str):
        self.account_id = account_id
        self.amount = amount
        self.status = status

    def to_json(self):
        return json.dumps({"account_id": self.account_id, "amount": str(self.amount), "status": self.status})
