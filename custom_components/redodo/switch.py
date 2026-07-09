"""Switch platform for Redodo."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import RedodoCoordinator
from .descriptions import SWITCHES
from .entity import RedodoEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Redodo switches."""

    coordinator: RedodoCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        RedodoSwitch(coordinator, description)
        for description in SWITCHES
    )


class RedodoSwitch(RedodoEntity, SwitchEntity):
    """Representation of a Redodo switch."""

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

    @property
    def is_on(self):
        """Return switch state."""

        value = self.get_register(
            self.entity_description.address
        )

        if value is None:
            return None

        return value == self.entity_description.on_value

    async def async_turn_on(self, **kwargs):
        """Turn switch on."""

        await self.write_register(
            self.entity_description.address,
            self.entity_description.on_value,
        )

        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn switch off."""

        await self.write_register(
            self.entity_description.address,
            self.entity_description.off_value,
        )

        await self.coordinator.async_request_refresh()