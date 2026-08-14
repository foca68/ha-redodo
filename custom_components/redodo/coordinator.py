"""Coordinator for Redodo."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN
from .modbus import RedodoModbus

_LOGGER = logging.getLogger(__name__)


class RedodoCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant, entry):

        self.hass = hass
        self.entry = entry

        self.modbus = RedodoModbus(
            port=entry.data["port"],
            slave=entry.data["slave"],
            baudrate=entry.data["baudrate"],
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=2),
        )

    async def _async_update_data(self):

        try:

            live = await self.modbus.read_holding_registers(
                256,
                35,
            )

            settings = await self.modbus.read_holding_registers(
                512,
                16,
            )

            today = await self.modbus.read_holding_registers(
                1024,
                5,
            )

            _LOGGER.warning("LIVE 256-290 : %s", live)
            _LOGGER.warning("SET  512-527 : %s", settings)
            _LOGGER.warning("DAY 1024-1028: %s", today)

            registers = {}

            for i, value in enumerate(live):
                registers[256 + i] = value

            for i, value in enumerate(settings):
                registers[512 + i] = value

            for i, value in enumerate(today):
                registers[1024 + i] = value

            return registers

        except Exception as err:
            raise UpdateFailed(err) from err

    def get(self, address: int):

        if self.data is None:
            return None

        return self.data.get(address)

    async def write_register(
        self,
        address: int,
        value: int,
    ):

        await self.modbus.write_register(
            address,
            value,
        )

        await self.async_request_refresh()