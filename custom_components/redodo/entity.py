"""Base entity for Redodo."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class RedodoEntity(CoordinatorEntity):
    """Base class: one device per config entry."""

    _attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        c = self.coordinator
        return DeviceInfo(
            identifiers={(DOMAIN, c.entry.entry_id)},
            name=c.entry.title,
            manufacturer="Redodo",
            model=c.model or "MPPT Solar Controller",
            sw_version=c.sw_version,
            hw_version=c.hw_version,
        )
