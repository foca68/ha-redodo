"""Switch platform for Redodo. """

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import RedodoEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            RedodoLoadSwitch(coordinator),
            RedodoLowTempSwitch(coordinator),
        ]
    )


class RedodoLoadSwitch(
    RedodoEntity,
    SwitchEntity,
):

    def __init__(self, coordinator):

        super().__init__(coordinator)

        self._attr_name = "Load Output"

        self._attr_unique_id = (
            f"{coordinator.entry.entry_id}_load_output"
        )

        self._address = 288

    @property
    def is_on(self):

        value = self.coordinator.get(self._address)

        return value == 1

    async def async_turn_on(self, **kwargs):

        await self.coordinator.write_register(
            self._address,
            1,
        )

    async def async_turn_off(self, **kwargs):

        await self.coordinator.write_register(
            self._address,
            0,
        )


class RedodoLowTempSwitch(
    RedodoEntity,
    SwitchEntity,
):

    def __init__(self, coordinator):

        super().__init__(coordinator)

        self._attr_name = "Low Temperature Protection"

        self._attr_unique_id = (
            f"{coordinator.entry.entry_id}_low_temperature"
        )

        self._address = 290

    @property
    def is_on(self):

        value = self.coordinator.get(self._address)

        return value == 1

    async def async_turn_on(self, **kwargs):

        await self.coordinator.write_register(
            self._address,
            1,
        )

    async def async_turn_off(self, **kwargs):

        await self.coordinator.write_register(
            self._address,
            0,
        )