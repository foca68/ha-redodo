"""Select platform for Redodo."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import RedodoCoordinator
from .descriptions import SELECTS
from .entity import RedodoEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Redodo selects."""

    coordinator: RedodoCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        RedodoSelect(coordinator, description)
        for description in SELECTS
    )


class RedodoSelect(RedodoEntity, SelectEntity):
    """Representation of a Redodo select."""

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

        self._attr_options = list(
            description.options.values()
        )

    @property
    def current_option(self):
        """Return current selected option."""

        value = self.get_register(
            self.entity_description.address
        )

        return self.entity_description.options.get(value)

    async def async_select_option(
        self,
        option: str,
    ) -> None:
        """Change selected option."""

        for key, value in self.entity_description.options.items():

            if value == option:

                await self.write_register(
                    self.entity_description.address,
                    key,
                )

                await self.coordinator.async_request_refresh()

                return