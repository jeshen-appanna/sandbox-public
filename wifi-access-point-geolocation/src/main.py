import hashlib
import json

import config
import requests
from dtos import APScanDto, GeolocationRequestDto
from fastapi import FastAPI, HTTPException, Request
from tenacity import retry, stop_after_attempt, wait_exponential

app = FastAPI()


def generate_cache_key(apscan_data: list[dict]) -> str:
    normalized_data = json.dumps(sorted(apscan_data, key=lambda apscan: apscan["bssid"]))
    return hashlib.sha256(normalized_data.encode()).hexdigest()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def post_geolocation_data(payload):
    response = requests.post(config.GOOGLE_API_URL, json=payload)
    response.raise_for_status()
    return response.json()


@app.post("/geolocate")
async def geolocate(request: Request):
    config.LOGGER.info("Received /geolocate request.")

    try:
        request_data = await request.json()
    except Exception as error:
        config.LOGGER.error(f"Invalid JSON body: {str(error)}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    if isinstance(request_data, list):
        request_data = request_data[0]

    if not isinstance(request_data, dict):
        raise HTTPException(status_code=400, detail="Input should be a valid dictionary")

    if "apscan_data" not in request_data:
        raise HTTPException(status_code=400, detail="Invalid request format")

    cache_key = generate_cache_key(request_data["apscan_data"])
    cached_result = config.MEMCACHE_CLIENT.get(cache_key)

    if cached_result:
        config.LOGGER.info(f"Returning cached result. Cache Key: {cache_key}")
        return json.loads(cached_result)

    apscan_data = [APScanDto.from_dictionary(apscan) for apscan in request_data["apscan_data"]]
    google_payload = GeolocationRequestDto.from_list(apscan_data)

    try:
        location_data = post_geolocation_data(google_payload)
    except requests.exceptions.RequestException as e:
        config.LOGGER.error(f"Google API Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Geolocation service unavailable")

    config.MEMCACHE_CLIENT.set(cache_key, json.dumps(location_data), expire=config.MEMCACHE_TLL)

    config.LOGGER.info("Returning /geolocate response.")

    return location_data
