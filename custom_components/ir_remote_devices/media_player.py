"""Media player platform for the IR Remote Devices integration."""

from __future__ import annotations

from typing import ClassVar

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .codes import (
    PIONEER_SOURCE_COMMANDS,
    PioneerReceiverCode,
    SamsungTVCode,
    make_pioneer_receiver_command,
    make_samsung_tv_command,
)
from .const import CONF_DEVICE_TYPE, CONF_INFRARED_ENTITY_ID, DeviceType
from .entity import IrRemoteDevicesEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up IR Remote Devices media players from a config entry."""
    infrared_entity_id = entry.data[CONF_INFRARED_ENTITY_ID]
    device_type = DeviceType(entry.data[CONF_DEVICE_TYPE])

    if device_type == DeviceType.SAMSUNG_TV:
        async_add_entities([SamsungTvMediaPlayer(entry, infrared_entity_id)])
    elif device_type == DeviceType.PIONEER_RECEIVER:
        async_add_entities([PioneerReceiverMediaPlayer(entry, infrared_entity_id)])


class SamsungTvMediaPlayer(IrRemoteDevicesEntity, MediaPlayerEntity):
    """Samsung TV media player controlled by IR."""

    _attr_name = None
    _attr_assumed_state = True
    _attr_device_class = MediaPlayerDeviceClass.TV
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON | MediaPlayerEntityFeature.TURN_OFF
    )

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        """Initialize a Samsung TV media player."""
        super().__init__(
            entry,
            infrared_entity_id,
            DeviceType.SAMSUNG_TV,
            unique_id_suffix="media_player",
        )
        self._attr_state = MediaPlayerState.ON

    async def async_turn_on(self) -> None:
        """Turn on the TV."""
        await self._send_command(make_samsung_tv_command(SamsungTVCode.POWER_ON))
        self._attr_state = MediaPlayerState.ON
        self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        """Turn off the TV."""
        await self._send_command(make_samsung_tv_command(SamsungTVCode.POWER_OFF))
        self._attr_state = MediaPlayerState.OFF
        self.async_write_ha_state()


class PioneerReceiverMediaPlayer(IrRemoteDevicesEntity, MediaPlayerEntity):
    """Pioneer receiver media player controlled by IR."""

    _attr_name = None
    _attr_assumed_state = True
    _attr_device_class = MediaPlayerDeviceClass.RECEIVER
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.VOLUME_STEP
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.SELECT_SOURCE
    )
    _attr_source_list: ClassVar[list[str]] = list(PIONEER_SOURCE_COMMANDS)

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        """Initialize a Pioneer receiver media player."""
        super().__init__(
            entry,
            infrared_entity_id,
            DeviceType.PIONEER_RECEIVER,
            unique_id_suffix="media_player",
        )
        self._attr_state = MediaPlayerState.ON
        self._attr_is_volume_muted = False

    async def async_turn_on(self) -> None:
        """Turn on the receiver."""
        await self._send_pioneer_code(PioneerReceiverCode.POWER_ON)
        self._attr_state = MediaPlayerState.ON
        self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        """Turn off the receiver."""
        await self._send_pioneer_code(PioneerReceiverCode.POWER_OFF)
        self._attr_state = MediaPlayerState.OFF
        self.async_write_ha_state()

    async def async_volume_up(self) -> None:
        """Send volume up command."""
        await self._send_pioneer_code(PioneerReceiverCode.VOLUME_UP)

    async def async_volume_down(self) -> None:
        """Send volume down command."""
        await self._send_pioneer_code(PioneerReceiverCode.VOLUME_DOWN)

    async def async_mute_volume(self, mute: bool) -> None:
        """Send mute command."""
        await self._send_pioneer_code(
            PioneerReceiverCode.MUTE_ON if mute else PioneerReceiverCode.MUTE_OFF,
        )
        self._attr_is_volume_muted = mute
        self.async_write_ha_state()

    async def async_select_source(self, source: str) -> None:
        """Select receiver source."""
        await self._send_pioneer_code(PIONEER_SOURCE_COMMANDS[source])
        self._attr_source = source
        self._attr_state = MediaPlayerState.ON
        self.async_write_ha_state()

    async def _send_pioneer_code(self, code: PioneerReceiverCode) -> None:
        """Send a Pioneer receiver command."""
        await self._send_command(make_pioneer_receiver_command(code))
