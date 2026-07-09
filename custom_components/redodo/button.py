"""Button platform for Redodo."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import RedodoCoordinator
from .descriptions import BUTTONS
from .entity import RedodoEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Redodo buttons."""

    coordinator: RedodoCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        RedodoButton(coordinator, description)
        for description in BUTTONS
    )


class RedodoButton(RedodoEntity, ButtonEntity):
    """Representation of a Redodo button."""

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

    async def async_press(self) -> None:
        """Execute button action."""

        await self.write_register(
            self.entity_description.address,
            self.entity_description.value,
        )

        await self.coordinator.async_request_refresh()