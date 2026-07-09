from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class RedodoEntity(CoordinatorEntity):

    def __init__(
        self,
        coordinator,
        name,
        unique_id,
    ):
        super().__init__(coordinator)

        self._attr_name = name
        self._attr_unique_id = unique_id

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={
                (DOMAIN, "redodo")
            },
            manufacturer="Redodo",
            model="MPPT Solar Controller",
            name="Redodo MPPT",
        )

    @property
    def available(self):
        return self.coordinator.last_update_success