"""Button platform for the IR Remote Devices integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from infrared_protocols import Command

from .codes import (
    PioneerReceiverCode,
    SamsungTVCode,
    make_pioneer_receiver_command,
    make_samsung_tv_command,
)
from .const import CONF_DEVICE_TYPE, CONF_INFRARED_ENTITY_ID, DeviceType
from .entity import IrRemoteDevicesEntity

PARALLEL_UPDATES = 1


@dataclass(frozen=True, kw_only=True)
class IrRemoteButtonEntityDescription(ButtonEntityDescription):
    """Describes an IR Remote Devices button entity."""

    command: Command


SAMSUNG_TV_BUTTON_DESCRIPTIONS: tuple[IrRemoteButtonEntityDescription, ...] = (
    IrRemoteButtonEntityDescription(
        key=SamsungTVCode.POWER_ON,
        translation_key="power_on",
        command=make_samsung_tv_command(SamsungTVCode.POWER_ON),
    ),
    IrRemoteButtonEntityDescription(
        key=SamsungTVCode.POWER_OFF,
        translation_key="power_off",
        command=make_samsung_tv_command(SamsungTVCode.POWER_OFF),
    ),
    IrRemoteButtonEntityDescription(
        key=SamsungTVCode.POWER_TOGGLE,
        translation_key="power_toggle",
        command=make_samsung_tv_command(SamsungTVCode.POWER_TOGGLE),
    ),
)

PIONEER_RECEIVER_BUTTON_DESCRIPTIONS: tuple[IrRemoteButtonEntityDescription, ...] = (
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.POWER_ON,
        translation_key="power_on",
        command=make_pioneer_receiver_command(PioneerReceiverCode.POWER_ON),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.POWER_OFF,
        translation_key="power_off",
        command=make_pioneer_receiver_command(PioneerReceiverCode.POWER_OFF),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.POWER_TOGGLE,
        translation_key="power_toggle",
        command=make_pioneer_receiver_command(PioneerReceiverCode.POWER_TOGGLE),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.MUTE_TOGGLE,
        translation_key="mute_toggle",
        command=make_pioneer_receiver_command(PioneerReceiverCode.MUTE_TOGGLE),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.MUTE_ON,
        translation_key="mute_on",
        command=make_pioneer_receiver_command(PioneerReceiverCode.MUTE_ON),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.MUTE_OFF,
        translation_key="mute_off",
        command=make_pioneer_receiver_command(PioneerReceiverCode.MUTE_OFF),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.VOLUME_UP,
        translation_key="volume_up",
        command=make_pioneer_receiver_command(PioneerReceiverCode.VOLUME_UP),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.VOLUME_DOWN,
        translation_key="volume_down",
        command=make_pioneer_receiver_command(PioneerReceiverCode.VOLUME_DOWN),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.TUNER,
        translation_key="tuner",
        command=make_pioneer_receiver_command(PioneerReceiverCode.TUNER),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.CD,
        translation_key="cd",
        command=make_pioneer_receiver_command(PioneerReceiverCode.CD),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.TV,
        translation_key="tv",
        command=make_pioneer_receiver_command(PioneerReceiverCode.TV),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.DVD,
        translation_key="dvd",
        command=make_pioneer_receiver_command(PioneerReceiverCode.DVD),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.SAT_CBL,
        translation_key="sat_cbl",
        command=make_pioneer_receiver_command(PioneerReceiverCode.SAT_CBL),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.GAME,
        translation_key="game",
        command=make_pioneer_receiver_command(PioneerReceiverCode.GAME),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.BD,
        translation_key="bd",
        command=make_pioneer_receiver_command(PioneerReceiverCode.BD),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.IPOD_USB,
        translation_key="ipod_usb",
        command=make_pioneer_receiver_command(PioneerReceiverCode.IPOD_USB),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.STATION_1,
        translation_key="station_1",
        command=make_pioneer_receiver_command(PioneerReceiverCode.STATION_1),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.STATION_2,
        translation_key="station_2",
        command=make_pioneer_receiver_command(PioneerReceiverCode.STATION_2),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.STATION_3,
        translation_key="station_3",
        command=make_pioneer_receiver_command(PioneerReceiverCode.STATION_3),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.STATION_4,
        translation_key="station_4",
        command=make_pioneer_receiver_command(PioneerReceiverCode.STATION_4),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.STATION_5,
        translation_key="station_5",
        command=make_pioneer_receiver_command(PioneerReceiverCode.STATION_5),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.STATION_6,
        translation_key="station_6",
        command=make_pioneer_receiver_command(PioneerReceiverCode.STATION_6),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.STATION_7,
        translation_key="station_7",
        command=make_pioneer_receiver_command(PioneerReceiverCode.STATION_7),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.STATION_8,
        translation_key="station_8",
        command=make_pioneer_receiver_command(PioneerReceiverCode.STATION_8),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.STATION_9,
        translation_key="station_9",
        command=make_pioneer_receiver_command(PioneerReceiverCode.STATION_9),
    ),
    IrRemoteButtonEntityDescription(
        key=PioneerReceiverCode.STATION_10,
        translation_key="station_10",
        command=make_pioneer_receiver_command(PioneerReceiverCode.STATION_10),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up IR Remote Devices buttons from a config entry."""
    infrared_entity_id = entry.data[CONF_INFRARED_ENTITY_ID]
    device_type = DeviceType(entry.data[CONF_DEVICE_TYPE])

    if device_type == DeviceType.SAMSUNG_TV:
        descriptions = SAMSUNG_TV_BUTTON_DESCRIPTIONS
    elif device_type == DeviceType.PIONEER_RECEIVER:
        descriptions = PIONEER_RECEIVER_BUTTON_DESCRIPTIONS
    else:
        descriptions = ()

    async_add_entities(
        IrRemoteButton(entry, infrared_entity_id, device_type, description)
        for description in descriptions
    )


class IrRemoteButton(IrRemoteDevicesEntity, ButtonEntity):
    """IR Remote Devices button entity."""

    entity_description: IrRemoteButtonEntityDescription

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_entity_id: str,
        device_type: DeviceType,
        description: IrRemoteButtonEntityDescription,
    ) -> None:
        """Initialize an IR Remote Devices button."""
        super().__init__(
            entry, infrared_entity_id, device_type, unique_id_suffix=description.key,
        )
        self.entity_description = description

    async def async_press(self) -> None:
        """Press the button."""
        await self._send_command(self.entity_description.command)

