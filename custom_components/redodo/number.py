"""Number platform for Redodo."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import RedodoEntity


NUMBERS = (
    ("system_voltage", "System Voltage", 514, 0, 2, 1),
    ("ovp_voltage", "Over Voltage Protection", 515, 10.0, 17.0, 0.1),
    ("equalize_voltage", "Equalize Voltage", 516, 10.0, 15.5, 0.1),
    ("boost_voltage", "Boost Voltage", 517, 10.0, 15.5, 0.1),
    ("float_voltage", "Float Voltage", 518, 10.0, 15.0, 0.1),
    ("boost_recovery", "Boost Recovery Voltage", 519, 10.0, 14.5, 0.1),
    ("overdischarge_reconnect", "Overdischarge Reconnect", 520, 10.0, 14.0, 0.1),
    ("under_voltage_warning", "Under Voltage Warning", 521, 10.0, 13.5, 0.1),
    ("overdischarge_disconnect", "Overdischarge Disconnect", 522, 10.0, 13.0, 0.1),
    ("discharge_limit", "Discharge Limit", 523, 9.0, 12.5, 0.1),
    ("load_mode", "Load Mode", 524, 0, 255, 1),
    ("light_delay", "Light Delay", 525, 0, 60, 1),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        RedodoNumber(
            coordinator,
            key,
            name,
            address,
            minimum,
            maximum,
            step,
        )
        for key, name, address, minimum, maximum, step in NUMBERS
    )


class RedodoNumber(
    RedodoEntity,
    NumberEntity,
):

    def __init__(
        self,
        coordinator,
        key,
        name,
        address,
        minimum,
        maximum,
        step,
    ):

        super().__init__(coordinator)

        self._address = address
        self._step = step

        self._attr_name = name
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}"

        self._attr_native_min_value = minimum
        self._attr_native_max_value = maximum
        self._attr_native_step = step

    @property
    def native_value(self):

        value = self.coordinator.get(self._address)

        if value is None:
            return None

        if self._step == 0.1:
            return value / 10

        return value

    async def async_set_native_value(self, value):

        if self._step == 0.1:
            value = int(round(value * 10))
        else:
            value = int(value)

        await self.coordinator.write_register(
            self._address,
            value,
        )