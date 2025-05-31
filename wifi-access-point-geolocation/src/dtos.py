from typing import Annotated

from pydantic import BaseModel

_DEFAULT_APSCAN_AGE = 0
_DEFAULT_APSCAN_SIGNAL_TO_NOISE_RATIO = 0


class APScanDto(BaseModel):
    mac_address: Annotated[str, "bssid"] = ...
    signal_strength: Annotated[int, "rssi"] = ...
    channel: Annotated[int, "channel"] = ...
    signal_to_noise_ratio: Annotated[int, "SNR"] = ...
    age: Annotated[int, "Age"] = ...

    def from_dictionary(apscan: dict) -> "APScanDto":
        return APScanDto(
            mac_address=apscan["bssid"],
            signal_strength=apscan["rssi"],
            channel=apscan["channel"],
            signal_to_noise_ratio=_DEFAULT_APSCAN_SIGNAL_TO_NOISE_RATIO,
            age=_DEFAULT_APSCAN_AGE,
        )


class GeolocationRequestDto(BaseModel):
    def from_list(apscan_data: list[APScanDto]) -> dict:
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
