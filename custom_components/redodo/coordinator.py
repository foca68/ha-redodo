from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN
from .modbus import RedodoModbus

_LOGGER = logging.getLogger(__name__)

class RedodoCoordinator(DataUpdateCoordinator):
    """Redodo Data Coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        port: str,
        slave: int,
        scan_interval: int,
    ):

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

        self.client = RedodoModbus(
            port=port,
            slave=slave,
        )

    async def _async_update_data(self):

        try:

            home = await self.hass.async_add_executor_job(
                self.client.read_home
            )

            settings = await self.hass.async_add_executor_job(
                self.client.read_settings
            )

            today = await self.hass.async_add_executor_job(
                self.client.read_today
            )

            return {
                "home": home,
                "settings": settings,
                "today": today,
            }

        except Exception as err:

            raise UpdateFailed(err) from err

    def get_home(self, index):

        return self.data["home"][index]

    def get_setting(self, index):

        return self.data["settings"][index]

    async def write_register(
        self,
        address,
        value,
    ):

        await self.hass.async_add_executor_job(
            self.client.write_single,
            address,
            value,
        )

        await self.async_request_refresh()

    async def write_registers(
        self,
        address,
        values,
    ):

        await self.hass.async_add_executor_job(
            self.client.write_multiple,
            address,
            values,
        )

        await self.async_request_refresh()

    async def async_shutdown(self):

        await self.hass.async_add_executor_job(
            self.client.close
        )

