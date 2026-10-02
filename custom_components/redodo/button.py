"""Button platform for Redodo.

All buttons are disabled by default (they change controller state).
"""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_SLAVE, DOMAIN, REG_FORCE_CHARGE
from .entity import RedodoEntity
from .utils import clear_history_frame, factory_reset_frame


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [RedodoForceChargeButton(c), RedodoClearHistoryButton(c), RedodoFactoryResetButton(c)]
    )


class _Button(RedodoEntity, ButtonEntity):
    _attr_entity_category = EntityCategory.CONFIG
    _attr_entity_registry_enabled_default = False

    def __init__(self, coordinator, key: str, name: str) -> None:
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_translation_key = key
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}"


class RedodoForceChargeButton(_Button):
    """Standard function 0x06: write 0x01FF to register 0x0121 (from BT capture)."""

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "force_charge", "Force Charge")

    async def async_press(self) -> None:
        await self.coordinator.write_register(REG_FORCE_CHARGE, 0x01FF)


class RedodoClearHistoryButton(_Button):
    """Proprietary function 0x79 - clears Today/Total energy statistics."""

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "clear_history", "Clear History")

    async def async_press(self) -> None:
        slave = self.coordinator.entry.data[CONF_SLAVE]
        await self.coordinator.send_raw(clear_history_frame(slave))


class RedodoFactoryResetButton(_Button):
    """Proprietary function 0x78 - restores factory settings."""

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "factory_reset", "Factory Reset")

    async def async_press(self) -> None:
        slave = self.coordinator.entry.data[CONF_SLAVE]
        await self.coordinator.send_raw(factory_reset_frame(slave))
