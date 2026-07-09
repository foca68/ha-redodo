"""Data coordinator for Redodo."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.const import CONF_BAUDRATE, CONF_PORT
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    HOME_COUNT,
    HOME_START,
    SETTING_COUNT,
    SETTING_START,
    TODAY_COUNT,
    TODAY_START,
)

from .modbus import RedodoModbus

_LOGGER = logging.getLogger(__name__)

CONF_SLAVE = "slave"


class RedodoCoordinator(DataUpdateCoordinator):
    """Redodo update coordinator."""

    def __init__(self, hass, entry):

        self.entry = entry

        self.modbus = RedodoModbus(
            port=entry.data[CONF_PORT],
            slave=entry.data[CONF_SLAVE],
            baudrate=entry.data[CONF_BAUDRATE],
        )

        self.home = {}
        self.settings = {}
        self.today = {}

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL
            ),
        )

    async def _async_update_data(self):
        """Read all controller registers."""

        try:

            #
            # HOME
            #

            values = await self.modbus.read_holding_registers(
                HOME_START,
                HOME_COUNT,
            )

            self.home = {
                HOME_START + i: value
                for i, value in enumerate(values)
            }

            #
            # SETTINGS
            #

            values = await self.modbus.read_holding_registers(
                SETTING_START,
                SETTING_COUNT,
            )

            self.settings = {
                SETTING_START + i: value
                for i, value in enumerate(values)
            }

            #
            # TODAY
            #

            values = await self.modbus.read_holding_registers(
                TODAY_START,
                TODAY_COUNT,
            )

            self.today = {
                TODAY_START + i: value
                for i, value in enumerate(values)
            }

            return True

        except Exception as err:

            raise UpdateFailed(err) from err

    def get_register(
        self,
        address: int,
        default=None,
    ):
        """Return cached register."""

        if address in self.home:
            return self.home[address]

        if address in self.settings:
            return self.settings[address]

        if address in self.today:
            return self.today[address]

        return default

    async def async_write_register(
        self,
        address: int,
        value: int,
    ):
        """Write one holding register."""

        await self.modbus.write_register(
            address,
            value,
        )

        await self.async_request_refresh()

    async def async_write_registers(
        self,
        address: int,
        values: list[int],
    ):
        """Write multiple holding registers."""

        await self.modbus.write_registers(
            address,
            values,
        )

        await self.async_request_refresh()

    async def async_shutdown(self):
        """Close serial connection."""

        await self.modbus.close()