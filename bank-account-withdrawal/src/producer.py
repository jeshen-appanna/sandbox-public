import json
import time

from config import KAFKA_BROKER, LOGGER
from events import WithdrawalEvent
from kafka import KafkaProducer

_PRODUCER = KafkaProducer(bootstrap_servers=KAFKA_BROKER, value_serializer=lambda v: json.dumps(v).encode("utf-8"))
_KAFKA_TOPIC = "bank_account_withdrawal"


def publish_event(event: WithdrawalEvent, retries: int = 3, backoff: int = 2):
    """Attempts to publish event with automatic retries."""
    attempt = 0
    while attempt < retries:
        try:
            _PRODUCER.send(_KAFKA_TOPIC, event.to_json())
        except Exception as error:
            LOGGER.error(f"Kafka publish failed: {error}, retrying in {backoff} sec...")
            # Exponential backoff
            time.sleep(backoff)
            # Double the wait time on each failure
            backoff *= 2
            attempt += 1
        else:
            _PRODUCER.flush()
            LOGGER.info("Event published to Kafka.")
            return

    LOGGER.error("Kafka event publishing failed after retries.")
