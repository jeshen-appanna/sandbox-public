"""
Database models for the Bank Account Withdrawal application.
"""

from sqlalchemy import create_engine, Column, BigInteger, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base

_DATABASE_URL = "sqlite:///bank.db"

Base = declarative_base()


class Account(Base):
    """
    Represents a bank account in the database.

    Attributes:
        id: Unique identifier for the account.
        balance: The account balance.
    """

    __tablename__ = "accounts"
    id = Column(BigInteger, primary_key=True)
    balance = Column(Numeric)


engine = create_engine(_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
