from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PORT, CONF_SCAN_INTERVAL

from .const import DOMAIN

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PORT): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=10): int,
        vol.Optional("slave", default=1): int,
    }
)

class RedodoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):

        if user_input is not None:

            await self.async_set_unique_id(user_input[CONF_PORT])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Redodo ({user_input[CONF_PORT]})",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
        )

