"""Manager module for handling geolocation request logic."""

import json

import config
import proxy
import utils
import validators
from dtos import WiFiAccessPointDto, GeolocationRequestDto
from fastapi import Request


async def process_geolocation_request(request: Request) -> dict:
    """
    Handles a single geolocation request.

    It parses the request body, validates the payload, checks for a cached response using a
    generated key, and if none is found, queries the external geolocation API. The response is
    cached and returned.

    Arguments:
        request: FastAPI request object containing JSON body.

    Returns:
        Geolocation result, either retrieved from cache or fetched from the external service.
    """
    request_data = await request.json()
    apscan_data = validators.validate_geolocation_request_payload(request_data)

    cache_key = utils.generate_cache_key(apscan_data)
    cached_data = config.MEMCACHE_CLIENT.get(cache_key)

    if cached_data:
        config.LOGGER.info(f"Cache hit. Key: {cache_key}")
        return json.loads(cached_data)

    apscan_dtos = [WiFiAccessPointDto.from_dictionary(apscan) for apscan in apscan_data]
    payload = GeolocationRequestDto.from_list(apscan_dtos)

    result = proxy.get_geolocation_data(payload)
    config.MEMCACHE_CLIENT.set(cache_key, json.dumps(result), expire=config.MEMCACHE_TLL)

    return result
