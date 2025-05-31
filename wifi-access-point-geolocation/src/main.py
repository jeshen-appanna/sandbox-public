"""Entry point for the Wi-Fi Access Point Geolocation API service."""

import config
import manager
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()


@app.post("/geolocate")
async def geolocate(request: Request):
    """
    Handle POST requests to the /geolocate endpoint.

    This route processes access point scan data received in the request body
    and returns the corresponding geolocation based on external API data.

    Arguments:
        request: The incoming FastAPI request object containing JSON data.

    Returns:
        A geolocation result, either retrieved from cache or from the Google API.

    Raises:
        HTTPException: If the request is invalid or an error occurs during processing.
    """
    config.LOGGER.info("Received /geolocate request.")
    try:
        return await manager.process_geolocation_request(request)
    except HTTPException as error:
        raise error
    except Exception as error:
        config.LOGGER.error(f"Unexpected error: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        config.LOGGER.info("Returned /geolocate response.")
