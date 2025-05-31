"""Validation module for input payloads in the geolocation service."""

from fastapi import HTTPException


def validate_geolocation_request_payload(data) -> list[dict]:
    """
    Validates the structure of the incoming geolocation request payload.

    Ensures the payload is a dictionary with a valid 'apscan_data' list field.
    If the input is a list, it extracts the first item for validation.

    Arguments:
        data: The raw request data, which can be a dictionary or a list containing a dictionary.

    Returns:
        The extracted and validated list of access point scan data.

    Raises:
        HTTPException: If the input format is invalid or required fields are missing.
    """
    if isinstance(data, list):
        data = data[0]

    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="Payload must be a dictionary")

    apscan_data = data.get("apscan_data")
    if not apscan_data or not isinstance(apscan_data, list):
        raise HTTPException(status_code=400, detail="Missing or invalid 'apscan_data' field")

    return apscan_data
