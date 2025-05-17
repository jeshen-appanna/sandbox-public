from decimal import Decimal
from enum import Enum

from config import LOGGER
from events import WithdrawalEvent
from models import Account, SessionLocal
from producer import publish_event
from sqlalchemy.exc import SQLAlchemyError

_ZERO_AMOUNT = Decimal("0")


class WithdrawalStatus(str, Enum):
    INVALID_AMOUNT = "invalid_withdrawal_amount"
    ACCOUNT_NOT_FOUND = "account_not_found"
    SUCCESS = "withdrawal_successful"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    TRANSACTION_FAILED = "transaction_failed"


class BankAccountController:
    def withdraw(account_id: int, amount: Decimal) -> WithdrawalStatus:
        if amount <= _ZERO_AMOUNT:
            LOGGER.warning("Invalid withdrawal amount.")
            return WithdrawalStatus.INVALID_AMOUNT

        session = SessionLocal()

        try:
            account = session.query(Account).filter(Account.id == account_id).with_for_update().first()

            if not account:
                LOGGER.error(f"Account {account_id} not found.")
                return WithdrawalStatus.ACCOUNT_NOT_FOUND

            if account.balance < amount:
                LOGGER.warning(f"Insufficient funds for account {account_id}.")
                return WithdrawalStatus.INSUFFICIENT_FUNDS

            account.balance -= amount
            session.commit()
            LOGGER.info(f"Withdrawal successful for account {account_id}, amount: {amount}.")

            publish_event(WithdrawalEvent(account_id=account_id, amount=amount, status=WithdrawalStatus.SUCCESS))
            return WithdrawalStatus.SUCCESS

        except SQLAlchemyError as error:
            session.rollback()
            LOGGER.error(f"Database error occurred: {error}")
            return WithdrawalStatus.TRANSACTION_FAILED

        finally:
            session.close()
