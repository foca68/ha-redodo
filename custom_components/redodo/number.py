"""Number platform: charge/discharge settings.

All numbers are disabled by default - writing wrong values to a charge
controller can damage a battery. Limits are given for a 12 V system and are
scaled automatically for 24 V / 48 V controllers (register 514).
"""

from __future__ import annotations

from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfElectricCurrent, UnitOfElectricPotential
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, REG_SYSTEM_VOLTAGE
from .entity import RedodoEntity

# key, name, address, min (12 V), max (12 V)
VOLTAGE_NUMBERS = (
    ("absorption_voltage", "Absorption Voltage", 516, 9.0, 16.5),
    ("equalization_voltage", "Equalization Voltage", 517, 9.0, 16.5),
    ("float_voltage", "Float Voltage", 518, 9.0, 16.5),
    ("boost_return_voltage", "Boost Return Voltage", 519, 9.0, 16.5),
    ("low_battery_warning", "Low Battery Warning", 520, 9.0, 16.5),
    ("low_battery_cutoff", "Low Battery Cutoff", 521, 9.0, 16.5),
    ("over_discharge_protection", "Over-discharge Protection", 522, 9.0, 16.5),
    ("discharge_reconnect", "Discharge Reconnect", 523, 9.0, 16.5),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    c = hass.data[DOMAIN][entry.entry_id]
    entities: list[NumberEntity] = [RedodoVoltageNumber(c, *n) for n in VOLTAGE_NUMBERS]
    entities.append(RedodoMaxCurrentNumber(c))
    async_add_entities(entities)


class _Base(RedodoEntity, NumberEntity):
    _attr_entity_category = EntityCategory.CONFIG
    _attr_entity_registry_enabled_default = False
    _attr_mode = NumberMode.BOX
    _address = 0

    def __init__(self, coordinator, key: str) -> None:
        super().__init__(coordinator)
        self._attr_translation_key = key
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}"


class RedodoVoltageNumber(_Base):
    """Voltage setting stored as volts x10."""

    _attr_device_class = NumberDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_native_step = 0.1

    def __init__(self, coordinator, key, name, address, vmin, vmax) -> None:
        super().__init__(coordinator, key)
        self._attr_name = name
        self._address = address
        self._vmin, self._vmax = vmin, vmax

    @property
    def _factor(self) -> float:
        sv = self.coordinator.get(REG_SYSTEM_VOLTAGE)
        return sv / 12 if sv in (12, 24, 48) else 1.0

    @property
    def native_min_value(self) -> float:
        return round(self._vmin * self._factor, 1)

    @property
    def native_max_value(self) -> float:
        return round(self._vmax * self._factor, 1)

    @property
    def native_value(self) -> float | None:
        raw = self.coordinator.get(self._address)
        return None if raw is None else round(raw / 10, 1)

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.write_register(self._address, int(round(value * 10)))


class RedodoMaxCurrentNumber(_Base):
    """Maximum charge current (A)."""

    _attr_name = "Max Charge Current"
    _attr_device_class = NumberDeviceClass.CURRENT
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_native_min_value = 1
    _attr_native_max_value = 40
    _attr_native_step = 1
    _address = 527

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "max_charge_current")

    @property
    def native_value(self) -> float | None:
        return self.coordinator.get(self._address)

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.write_register(self._address, int(value))
