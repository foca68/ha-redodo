"""Base entity for Redodo."""

from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import RedodoCoordinator


class RedodoEntity(CoordinatorEntity):
    """Base Redodo entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: RedodoCoordinator,
        name: str,
        unique: str,
    ) -> None:

        super().__init__(coordinator)

        self._attr_name = name

        self._attr_unique_id = unique

    @property
    def available(self) -> bool:
        """Return availability."""

        return self.coordinator.last_update_success

    def get_register(
        self,
        address: int,
        default=None,
    ):
        """Return register value."""

        return self.coordinator.get_register(
            address,
            default,
        )

    async def write_register(
        self,
        address: int,
        value: int,
    ):
        """Write one register."""

        await self.coordinator.async_write_register(
            address,
            value,
        )

    async def write_registers(
        self,
        address: int,
        values: list[int],
    ):
        """Write multiple registers."""

        await self.coordinator.async_write_registers(
            address,
            values,
        )