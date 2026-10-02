"""Switch platform for Redodo."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, REG_LOAD_SWITCH
from .entity import RedodoEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([RedodoLoadSwitch(hass.data[DOMAIN][entry.entry_id])])


class RedodoLoadSwitch(RedodoEntity, SwitchEntity):
    """DC load output on/off (register 288)."""

    _attr_name = "Load Output"
    _attr_translation_key = "load_output"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_load_output"

    @property
    def is_on(self) -> bool | None:
        value = self.coordinator.get(REG_LOAD_SWITCH)
        return None if value is None else value == 1

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.write_register(REG_LOAD_SWITCH, 1)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.write_register(REG_LOAD_SWITCH, 0)
