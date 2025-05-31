"""Data Transfer Objects (DTOs) for the Wi-Fi Access Point Geolocation service."""

from typing import Annotated

from pydantic import BaseModel

_DEFAULT_APSCAN_AGE = 0
"""Default value for signal age in the access point scan."""

_DEFAULT_APSCAN_SIGNAL_TO_NOISE_RATIO = 0
"""Default value for signal-to-noise ratio in the access point scan."""


class WiFiAccessPointDto(BaseModel):
    """Represents a single Wi-Fi access point observation from a scan."""

    mac_address: Annotated[str, "The MAC address (BSSID) of the access point."] = ...
    signal_strength: Annotated[int, "Received signal strength indication (RSSI)"] = ...
    channel: Annotated[int, "Channel on which the AP is broadcasting"] = ...
    signal_to_noise_ratio: Annotated[int, "Signal-to-noise ratio"] = ...
    age: Annotated[int, "Time in milliseconds since this scan was performed"] = ...

    @classmethod
    def from_dictionary(cls, apscan: dict) -> "WiFiAccessPointDto":
        """
        Converts a raw dictionary representing a scanned access point into a DTO.

        Arguments:
            apscan: A dictionary containing raw access point scan data.

        Returns:
            A populated data transfer object.
        """
        return WiFiAccessPointDto(
            mac_address=apscan["bssid"],
            signal_strength=apscan["rssi"],
            channel=apscan["channel"],
            signal_to_noise_ratio=_DEFAULT_APSCAN_SIGNAL_TO_NOISE_RATIO,
            age=_DEFAULT_APSCAN_AGE,
        )


class GeolocationRequestDto(BaseModel):
    """Constructs the payload required by the Google Geolocation API."""

    @classmethod
    def from_list(cls, apscan_data: list[WiFiAccessPointDto]) -> dict:
        """
        Converts a list of access point DTOs into the Google API payload format.

        Arguments:
            apscan_data: A list of validated access point objects.

        Returns:
            A dictionary formatted for submission to the Google Geolocation API.
        """
        return {
            "wifiAccessPoints": [
                {
                    "macAddress": apscan.mac_address,
                    "signalStrength": apscan.signal_strength,
                    "signalToNoiseRatio": apscan.signal_to_noise_ratio,
                    "channel": apscan.channel,
                    "age": apscan.age,
                }
                for apscan in apscan_data
            ]
        }
