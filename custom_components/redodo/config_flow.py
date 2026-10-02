"""Config flow for Redodo."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_PORT
from homeassistant.core import callback

from .const import (
    CONF_BAUDRATE,
    CONF_SCAN_INTERVAL,
    CONF_SLAVE,
    DEFAULT_BAUDRATE,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SLAVE,
    DOMAIN,
)
from .modbus import RedodoModbus


async def _can_connect(port: str, slave: int, baudrate: int) -> bool:
    """Try to read the battery SOC register once."""
    client = RedodoModbus(port, slave, baudrate)
    try:
        await client.read_holding_registers(257, 1)
        return True
    except Exception:  # noqa: BLE001
        return False
    finally:
        await client.close()


class RedodoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Redodo."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_PORT]}_{user_input[CONF_SLAVE]}"
            )
            self._abort_if_unique_id_configured()

            if await _can_connect(
                user_input[CONF_PORT], user_input[CONF_SLAVE], user_input[CONF_BAUDRATE]
            ):
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
            errors["base"] = "cannot_connect"

        d = user_input or {}
        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=d.get(CONF_NAME, DEFAULT_NAME)): str,
                vol.Required(CONF_PORT, default=d.get(CONF_PORT, DEFAULT_PORT)): str,
                vol.Required(CONF_SLAVE, default=d.get(CONF_SLAVE, DEFAULT_SLAVE)): vol.All(
                    vol.Coerce(int), vol.Range(min=1, max=247)
                ),
                vol.Required(
                    CONF_BAUDRATE, default=d.get(CONF_BAUDRATE, DEFAULT_BAUDRATE)
                ): vol.In([9600, 19200, 38400, 57600, 115200]),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return RedodoOptionsFlow()


class RedodoOptionsFlow(config_entries.OptionsFlow):
    """Polling interval option."""

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        current = self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        schema = vol.Schema(
            {
                vol.Required(CONF_SCAN_INTERVAL, default=current): vol.All(
                    vol.Coerce(int), vol.Range(min=1, max=300)
                )
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
