"""Select platform for Redodo. """

# from __future__ import annotations

# from homeassistant.components.select import SelectEntity
# from homeassistant.config_entries import ConfigEntry
# from homeassistant.core import HomeAssistant
# from homeassistant.helpers.entity_platform import AddEntitiesCallback

# from .const import DOMAIN
# from .entity import RedodoEntity


# BATTERY_TYPES = [
    # "User",
    # "Sealed",
    # "Gel",
    # "Flooded",
    # "Lithium LiFePO4",
# ]


# async def async_setup_entry(
    # hass: HomeAssistant,
    # entry: ConfigEntry,
    # async_add_entities: AddEntitiesCallback,
# ) -> None:

    # coordinator = hass.data[DOMAIN][entry.entry_id]

    # async_add_entities(
        # [
            # RedodoBatteryTypeSelect(
                # coordinator,
            # )
        # ]
    # )


# class RedodoBatteryTypeSelect(
    # RedodoEntity,
    # SelectEntity,
# ):

    # def __init__(
        # self,
        # coordinator,
    # ):

        # super().__init__(coordinator)

        # self._address = 513

        # self._attr_name = "Battery Type"

        # self._attr_unique_id = (
            # f"{coordinator.entry.entry_id}_battery_type"
        # )

        # self._attr_options = BATTERY_TYPES

    # @property
    # def current_option(self):

        # value = self.coordinator.get(self._address)

        # if value is None:
            # return None

        # if value >= len(BATTERY_TYPES):
            # return None

        # return BATTERY_TYPES[value]

    # async def async_select_option(
        # self,
        # option: str,
    # ):

        # value = BATTERY_TYPES.index(option)

        # await self.coordinator.write_register(
            # self._address,
            # value,
        # )