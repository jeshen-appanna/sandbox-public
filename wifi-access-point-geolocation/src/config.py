import os

import structlog
from dotenv import load_dotenv
from pymemcache.client.base import Client


# Load environment variables
load_dotenv()

# Configure structured logging
structlog.configure(processors=[structlog.processors.TimeStamper(fmt="iso"), structlog.processors.JSONRenderer()])

LOGGER = structlog.get_logger()
MEMCACHE_CLIENT = Client(("memcached", 11211))
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_URL = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}"
