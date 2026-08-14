"""Base entity for Redodo. """

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class RedodoEntity(CoordinatorEntity):

    def __init__(self, coordinator) -> None:
        """Initialize Redodo entity."""
        super().__init__(coordinator)

        self._attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self.coordinator.entry.entry_id,
                )
            },
            name=self.coordinator.entry.title,
            manufacturer="Redodo",
            model="MPPT Solar Controller",
        )

    @property
    def available(self) -> bool:
        """Return availability."""
        return self.coordinator.last_update_success