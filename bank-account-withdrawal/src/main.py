"""Main module for the Bank Account Withdrawal application."""

from decimal import Decimal
from random import randint

from prettytable import PrettyTable
from sqlalchemy.dialects.sqlite import insert

import config
from models import Account, SessionLocal
from controller import BankAccountController


def initialize_sample_data() -> None:
    """
    Populates the database with sample account data.

    Creates five accounts with random balances and ensures duplicates
    are ignored when inserting records.
    """
    with SessionLocal() as session:
        for id in range(1, 6):
            statement = (
                insert(Account)
                .values(
                    customer_id=id * 9099,
                    balance=Decimal(str(randint(100, 1000))),
                )
                .prefix_with("OR IGNORE")
            )
            session.execute(statement)
        session.commit()


def get_all_accounts() -> list[Account]:
    """
    Retrieves all bank accounts from the database.

    Returns:
        A list of account objects, sorted by account ID.
    """
    with SessionLocal() as session:
        return session.query(Account).order_by(Account.id).all()


def print_accounts(accounts: list[Account]) -> None:
    """
    Displays all accounts and their balances in a formatted table.

    Arguments:
        accounts: List of account objects to display.
    """
    table = PrettyTable()
    table.field_names = ["Account ID", "Customer ID", "Balance", "Date Created", "Date Modified"]

    for account in accounts:
        table.add_row(
            [account.id, account.customer_id, f"{account.balance:.2f}", account.date_created, account.date_modified]
        )
    print(table)


def main():
    """
    Runs the Bank Account Withdrawal application.

    Initializes the database, populates sample accounts, and provides an interactive
    command-line interface for users to withdraw funds.
    """
    config.initialize_database()
    initialize_sample_data()

    while True:
        print("\nAvailable Accounts:")
        accounts = get_all_accounts()
        print_accounts(accounts)

        try:
            account_id = int(input("Enter Account ID to withdraw money from: "))
            amount = Decimal(input("Enter amount to withdraw: "))
        except (ValueError, Decimal.InvalidOperation) as error:
            print(f"Invalid input: {error}")
        else:
            BankAccountController.withdraw(account_id=account_id, amount=amount)

        again = input("Do you want to perform another withdrawal? (y/n): ").strip().lower()
        if again != "y":
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
