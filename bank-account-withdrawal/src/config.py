import logging

from models import Base, engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bank_account_withdrawal.log"), logging.StreamHandler()],
)

# Global constants
LOGGER = logging.getLogger(__name__)
KAFKA_BROKER = "localhost:9092"


def initialize_database():
    Base.metadata.create_all(engine)
    print("Database and table initialized successfully.")
