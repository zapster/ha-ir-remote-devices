"""Constants for the IR Remote Devices integration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

DOMAIN = "ir_remote_devices"

CONF_DEVICE_TYPE = "device_type"
CONF_INFRARED_ENTITY_ID = "infrared_entity_id"


class DeviceType(StrEnum):
    """Supported IR device profiles."""

    SAMSUNG_TV = "samsung_tv"
    PIONEER_RECEIVER = "pioneer_receiver"


@dataclass(frozen=True, slots=True)
class DeviceProfile:
    """Static metadata for an IR device profile."""

    name: str
    manufacturer: str
    model: str | None = None


DEVICE_PROFILES: dict[DeviceType, DeviceProfile] = {
    DeviceType.SAMSUNG_TV: DeviceProfile(
        name="Samsung TV",
        manufacturer="Samsung",
    ),
    DeviceType.PIONEER_RECEIVER: DeviceProfile(
        name="Pioneer Receiver",
        manufacturer="Pioneer",
    ),
}

