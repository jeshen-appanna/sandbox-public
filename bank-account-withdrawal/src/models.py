"""
Database models for the Bank Account Withdrawal application.
"""

from datetime import datetime

import config
from sqlalchemy import Integer, Column, DateTime, Numeric, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

_DATABASE_URL = "sqlite:///bank.db"

Base = declarative_base()


class Account(Base):
    """
    Represents a bank account in the database.

    Attributes:
        id: Unique identifier for the account.
        customer_id: ID of the customer associated with the account.
        balance: Account balance.
        date_created: Timestamp when the account was created.
        date_modified: Timestamp of the last modification.
    """

    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    balance = Column(Numeric(10, 2), nullable=False, default=0)
    date_created = Column(DateTime, default=lambda: datetime.now(config.SAST_TIMEZONE))
    date_modified = Column(
        DateTime,
        default=lambda: datetime.now(config.SAST_TIMEZONE),
        onupdate=lambda: datetime.now(config.SAST_TIMEZONE),
    )


engine = create_engine(_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
