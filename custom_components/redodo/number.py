"""Number platform for Redodo."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import RedodoCoordinator
from .descriptions import NUMBERS
from .entity import RedodoEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Redodo numbers."""

    coordinator: RedodoCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        RedodoNumber(coordinator, description)
        for description in NUMBERS
    )


class RedodoNumber(RedodoEntity, NumberEntity):
    """Representation of a Redodo number."""

    def __init__(
        self,
        coordinator: RedodoCoordinator,
        description,
    ) -> None:

        super().__init__(
            coordinator,
            description.name,
            description.key,
        )

        self.entity_description = description

        self._attr_native_min_value = description.minimum
        self._attr_native_max_value = description.maximum
        self._attr_native_step = description.step
        self._attr_native_unit_of_measurement = description.unit

    @property
    def native_value(self):
        """Return current value."""

        value = self.get_register(
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

    async def async_set_native_value(
        self,
        value: float,
    ) -> None:
        """Write new value."""

        register_value = value

        if self.entity_description.scale != 1:
            register_value = round(
                value / self.entity_description.scale
            )

        await self.write_register(
            self.entity_description.address,
            int(register_value),
        )

        await self.coordinator.async_request_refresh()