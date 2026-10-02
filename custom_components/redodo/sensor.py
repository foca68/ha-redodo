"""Sensor platform for Redodo."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .descriptions import SENSORS, RedodoSensorDescription
from .entity import RedodoEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(RedodoSensor(coordinator, d) for d in SENSORS)


class RedodoSensor(RedodoEntity, SensorEntity):
    """Generic register-backed sensor."""

    entity_description: RedodoSensorDescription

    def __init__(self, coordinator, description: RedodoSensorDescription) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{description.key}"

    @property
    def native_value(self):
        regs = self.coordinator.data
        if not regs:
            return None
        d = self.entity_description
        if d.value_fn is not None:
            return d.value_fn(regs)
        raw = regs.get(d.address)
        if raw is None:
            return None
        if d.scale != 1:
            return round(raw * d.scale, 3)
        return raw
