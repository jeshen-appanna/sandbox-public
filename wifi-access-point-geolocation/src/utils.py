"""Utility module providing helper functions for the geolocation service."""

import hashlib
import json


def generate_cache_key(apscan_data: list[dict]) -> str:
    """
    Generates a SHA-256 hash key from sorted access point scan data.

    This is used to create a unique and consistent cache key for a given set of Wi-Fi access points.

    Args:
        apscan_data: List of access point dictionaries, each containing at least a 'bssid'.

    Returns:
        A SHA-256 hexadecimal string representing the cache key.
    """
    normalized_data = json.dumps(sorted(apscan_data, key=lambda apscan: apscan["bssid"]))
    return hashlib.sha256(normalized_data.encode()).hexdigest()
