"""Coordinator for Redodo."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_BAUDRATE,
    CONF_SCAN_INTERVAL,
    CONF_SLAVE,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    INFO_COUNT,
    INFO_START,
    LIVE_COUNT,
    LIVE_START,
    SETTING_COUNT,
    SETTING_START,
    SETTINGS_EVERY,
    TODAY_COUNT,
    TODAY_START,
)
from .modbus import RedodoModbus
from .utils import ascii_from_registers

_LOGGER = logging.getLogger(__name__)


class RedodoCoordinator(DataUpdateCoordinator[dict[int, int]]):
    """Poll the controller and keep all registers in one dict."""

    def __init__(self, hass: HomeAssistant, entry) -> None:
        interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=timedelta(seconds=interval),
        )
        self.entry = entry
        self.modbus = RedodoModbus(
            port=entry.data["port"],
            slave=entry.data[CONF_SLAVE],
            baudrate=entry.data[CONF_BAUDRATE],
        )
        self._registers: dict[int, int] = {}
        self._cycle = 0
        self.model: str | None = None
        self.hw_version: str | None = None
        self.sw_version: str | None = None

    def _store(self, start: int, values: list[int]) -> None:
        for i, value in enumerate(values):
            self._registers[start + i] = value

    async def _read_optional(self, start: int, count: int) -> list[int] | None:
        """Read a non-critical block; a failure must not break the live data."""
        try:
            return await self.modbus.read_holding_registers(start, count)
        except Exception as err:  # noqa: BLE001
            _LOGGER.debug("Optional block %s+%s failed: %s", start, count, err)
            return None

    async def _async_update_data(self) -> dict[int, int]:
        try:
            self._store(
                LIVE_START,
                await self.modbus.read_holding_registers(LIVE_START, LIVE_COUNT),
            )
        except Exception as err:
            raise UpdateFailed(err) from err

        if values := await self._read_optional(TODAY_START, TODAY_COUNT):
            self._store(TODAY_START, values)

        if self._cycle % SETTINGS_EVERY == 0:
            if values := await self._read_optional(SETTING_START, SETTING_COUNT):
                self._store(SETTING_START, values)
            if self.model is None and (
                values := await self._read_optional(INFO_START, INFO_COUNT)
            ):
                self._store(INFO_START, values)
                self.hw_version = str(values[0])
                self.sw_version = str(values[1])
                self.model = ascii_from_registers(values[2:9]) or None
        self._cycle += 1
        return dict(self._registers)

    def get(self, address: int) -> int | None:
        if self.data is None:
            return None
        return self.data.get(address)

    async def write_register(self, address: int, value: int) -> None:
        await self.modbus.write_register(address, value)
        self._registers[address] = value
        self.async_set_updated_data(dict(self._registers))
        await self.async_request_refresh()

    async def send_raw(self, frame: bytes) -> None:
        await self.modbus.raw_command(frame)
        await self.async_request_refresh()
