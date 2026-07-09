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
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [RedodoSensor(coordinator, description) for description in SENSORS]
    )


class RedodoSensor(
    RedodoEntity,
    SensorEntity,
):

    def __init__(
        self,
        coordinator,
        description: RedodoSensorDescription,
    ) -> None:

        super().__init__(coordinator)

        self.entity_description = description

        self._attr_unique_id = (
            f"{coordinator.entry.entry_id}_{description.key}"
        )

    @property
    def native_value(self):

        value = self.coordinator.get(
            self.entity_description.address
        )

        if value is None:
            return None

        if self.entity_description.scale != 1:
            return round(
                value * self.entity_description.scale,
                2,
            )

        return value