"""Config flow for the IR Remote Devices integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.components.infrared import (
    DOMAIN as INFRARED_DOMAIN,
)
from homeassistant.components.infrared import (
    async_get_emitters,
)
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_DEVICE_TYPE,
    CONF_INFRARED_ENTITY_ID,
    DEVICE_PROFILES,
    DOMAIN,
    DeviceType,
)


class IrRemoteDevicesConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle config flow for IR Remote Devices."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        emitter_entity_ids = async_get_emitters(self.hass)
        if not emitter_entity_ids:
            return self.async_abort(reason="no_emitters")

        if user_input is not None:
            entity_id = user_input[CONF_INFRARED_ENTITY_ID]
            device_type = DeviceType(user_input[CONF_DEVICE_TYPE])

            await self.async_set_unique_id(f"{device_type}_{entity_id}")
            self._abort_if_unique_id_configured()

            ent_reg = er.async_get(self.hass)
            registry_entry = ent_reg.async_get(entity_id)
            entity_name = (
                registry_entry.name or registry_entry.original_name or entity_id
                if registry_entry
                else entity_id
            )

            title = f"{DEVICE_PROFILES[device_type].name} via {entity_name}"
            return self.async_create_entry(title=title, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICE_TYPE): SelectSelector(
                        SelectSelectorConfig(
                            options=[device_type.value for device_type in DeviceType],
                            translation_key=CONF_DEVICE_TYPE,
                            mode=SelectSelectorMode.DROPDOWN,
                        ),
                    ),
                    vol.Required(CONF_INFRARED_ENTITY_ID): EntitySelector(
                        EntitySelectorConfig(
                            domain=INFRARED_DOMAIN,
                            include_entities=emitter_entity_ids,
                        ),
                    ),
                },
            ),
        )

