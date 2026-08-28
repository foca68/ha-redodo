"""Button platform for Redodo."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import RedodoEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            # RedodoForceChargeButton(coordinator),
            RedodoClearHistoryButton(coordinator),
            # RedodoFactoryResetButton(coordinator),
        ]
    )


class RedodoButton(
    RedodoEntity,
    ButtonEntity,
):

    def __init__(
        self,
        coordinator,
        key,
        name,
    ):

        super().__init__(coordinator)

        self._attr_name = name

        self._attr_unique_id = (
            f"{coordinator.entry.entry_id}_{key}"
        )


class RedodoForceChargeButton(RedodoButton):

    def __init__(self, coordinator):

        super().__init__(
            coordinator,
            "force_charge",
            "Force Charge",
        )

    async def async_press(self):

        #
        # TODO
        # Proprietary command:
        # 01 06 01 21 01 FF
        #
        raise NotImplementedError(
            "Force Charge command not implemented"
        )


class RedodoClearHistoryButton(RedodoButton):

    def __init__(self, coordinator):

        super().__init__(
            coordinator,
            "clear_history",
            "Clear History",
        )

    async def async_press(self):

        #
        # TODO
        # Proprietary command:
        # 01 79 FF FF FF FF
        #
        raise NotImplementedError(
            "Clear History command not implemented"
        )


class RedodoFactoryResetButton(RedodoButton):

    def __init__(self, coordinator):

        super().__init__(
            coordinator,
            "factory_reset",
            "Factory Reset",
        )

    async def async_press(self):

        #
        # TODO
        # Proprietary command:
        # 01 78 FF FF FF FF
        #
        raise NotImplementedError(
            "Factory Reset command not implemented"
        )