from decimal import Decimal
from random import randint

from prettytable import PrettyTable
from sqlalchemy.dialects.sqlite import insert

import config
from models import Account, SessionLocal
from controller import BankAccountController


def initialize_sample_data() -> None:
    with SessionLocal() as session:
        for account_id in range(1, 6):
            statement = (
                insert(Account)
                .values(
                    id=account_id,
                    balance=Decimal(str(randint(100, 1000))),
                )
                .prefix_with("OR IGNORE")
            )
            session.execute(statement)
        session.commit()


def get_all_accounts() -> list[Account]:
    with SessionLocal() as session:
        return session.query(Account).order_by(Account.id).all()


def print_accounts(accounts: list[Account]) -> None:
    table = PrettyTable()
    table.field_names = ["Account ID", "Balance"]

    for account in accounts:
        table.add_row([account.id, f"{account.balance:.2f}"])
    print(table)


def main():
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
