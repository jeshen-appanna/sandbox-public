"""Proxy module responsible for communication with the external Google Geolocation API."""

import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import config

# Retry configuration: maximum 3 attempts, with exponential wait (2s, 4s, up to 10s max)
_RETRY_DEFAULT_STOP = stop_after_attempt(3)
_RETRY_DEFAULT_WAIT = wait_exponential(multiplier=1, min=2, max=10)


@retry(stop=_RETRY_DEFAULT_STOP, wait=_RETRY_DEFAULT_WAIT)
def get_geolocation_data(payload: dict) -> dict:
    """
    Sends a geolocation request to the Google API with retry logic.

    Arguments:
        payload: The payload containing Wi-Fi access point data.

    Returns:
        JSON response containing geolocation data.

    Raises:
        requests.exceptions.RequestException: If the API call fails after retries.
    """
    response = requests.post(config.GOOGLE_API_URL, json=payload)
    response.raise_for_status()
    return response.json()
