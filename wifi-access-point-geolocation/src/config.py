"""Configuration module for the Wi-Fi Access Point Geolocation service."""

import os

import structlog
from dotenv import load_dotenv
from pymemcache.client.base import Client

load_dotenv()
structlog.configure(processors=[structlog.processors.TimeStamper(fmt="iso"), structlog.processors.JSONRenderer()])


LOGGER = structlog.get_logger()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_URL = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}"

# Cache (Time to live is in seconds) (1 hour)
MEMCACHE_CLIENT = Client(("memcached", 11211))
MEMCACHE_TLL = 3600
