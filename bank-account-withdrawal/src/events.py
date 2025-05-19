"""Events module for the Bank Account Withdrawal application."""

import json
from datetime import datetime
from decimal import Decimal

from config import SAST_TIMEZONE


class WithdrawalEvent:
    """Represents a withdrawal event in the banking system."""

    def __init__(self, account_id: int, amount: Decimal, status: str):
        """
        Initializes a WithdrawalEvent instance.

        Arguments:
            account_id: The unique identifier for the account.
            amount: The amount withdrawn.
            status: The status of the withdrawal transaction.
            timestamp: The timestamp of the event in ISO format (SAST).
        """
        self.account_id = account_id
        self.amount = amount
        self.status = status
        self.timestamp = datetime.now(SAST_TIMEZONE).isoformat()

    def to_json(self):
        """
        Serializes the withdrawal event into a JSON string.

        Returns:
            The serialized JSON representation of the withdrawal event.
        """
        return json.dumps(
            {
                "account_id": self.account_id,
                "amount": str(self.amount),
                "status": self.status,
                "timestamp": self.timestamp,
            }
        )
