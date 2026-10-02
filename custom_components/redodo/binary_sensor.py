"""Binary sensors for Redodo."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import RedodoEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([RedodoChargingBinarySensor(hass.data[DOMAIN][entry.entry_id])])


class RedodoChargingBinarySensor(RedodoEntity, BinarySensorEntity):
    """On while the battery receives charge current."""

    _attr_name = "Charging"
    _attr_translation_key = "charging"
    _attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_charging"

    @property
    def is_on(self) -> bool | None:
        value = self.coordinator.get(259)  # charge current x100
        return None if value is None else value > 0
