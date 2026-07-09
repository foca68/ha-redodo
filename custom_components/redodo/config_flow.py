"""Config flow for Redodo."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_PORT

from .const import (
    DEFAULT_BAUDRATE,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SLAVE,
    DOMAIN,
)

CONF_SLAVE = "slave"
CONF_BAUDRATE = "baudrate"


class RedodoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Redodo."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        if user_input is not None:

            await self.async_set_unique_id(
                f"{user_input[CONF_PORT]}_{user_input[CONF_SLAVE]}"
            )

            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_NAME,
                    default=DEFAULT_NAME,
                ): str,

                vol.Required(
                    CONF_PORT,
                    default=DEFAULT_PORT,
                ): str,

                vol.Required(
                    CONF_SLAVE,
                    default=DEFAULT_SLAVE,
                ): vol.Coerce(int),

                vol.Required(
                    CONF_BAUDRATE,
                    default=DEFAULT_BAUDRATE,
                ): vol.In(
                    [
                        9600,
                        19200,
                        38400,
                        57600,
                        115200,
                    ]
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )