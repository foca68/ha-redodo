"""Entity descriptions for Redodo (decimal Modbus holding-register addresses)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
)

from .const import REG_STATUS_1, REG_STATUS_2, REG_SYSTEM_VOLTAGE, REG_TEMPS
from .utils import (
    ascii_from_registers,
    battery_temp,
    battery_type_text,
    controller_temp,
)


@dataclass(frozen=True, kw_only=True)
class RedodoSensorDescription(SensorEntityDescription):
    """Redodo sensor description."""

    address: int = 0
    scale: float = 1.0
    value_fn: Callable[[dict[int, int]], Any] | None = None


def _s(key: str, name: str, address: int = 0, **kw: Any) -> RedodoSensorDescription:
    return RedodoSensorDescription(
        key=key, name=name, translation_key=key, address=address, **kw
    )


_MEAS = SensorStateClass.MEASUREMENT
_VOLT = dict(
    device_class=SensorDeviceClass.VOLTAGE,
    native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    state_class=_MEAS,
    suggested_display_precision=1,
)
_DIAG = dict(entity_category=EntityCategory.DIAGNOSTIC)
_HIDDEN = dict(entity_category=EntityCategory.DIAGNOSTIC, entity_registry_enabled_default=False)


def _opt(fn: Callable[[dict[int, int]], Any], *addrs: int):
    """Wrap fn so it returns None while any needed register is missing."""
    return lambda r: fn(r) if all(a in r for a in addrs) else None


SENSORS: tuple[RedodoSensorDescription, ...] = (
    # --- Battery ---------------------------------------------------------
    _s("battery_soc", "Battery SOC", 257,
       device_class=SensorDeviceClass.BATTERY,
       native_unit_of_measurement="%", state_class=_MEAS),
    _s("battery_voltage", "Battery Voltage", 258, scale=0.1, **_VOLT),
    _s("charge_current", "Charge Current", 259, scale=0.01,
       suggested_display_precision=2,
       device_class=SensorDeviceClass.CURRENT,
       native_unit_of_measurement=UnitOfElectricCurrent.AMPERE, state_class=_MEAS),
    _s("charge_power", "Charge Power", 260,
       device_class=SensorDeviceClass.POWER,
       native_unit_of_measurement=UnitOfPower.WATT, state_class=_MEAS),
    # Register 261 packs two temperatures: high byte = controller, low byte = battery
    _s("battery_temperature", "Battery Temperature",
       value_fn=_opt(lambda r: battery_temp(r[REG_TEMPS]), REG_TEMPS),
       device_class=SensorDeviceClass.TEMPERATURE,
       native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=_MEAS),
    _s("controller_temperature", "Controller Temperature",
       value_fn=_opt(lambda r: controller_temp(r[REG_TEMPS]), REG_TEMPS),
       device_class=SensorDeviceClass.TEMPERATURE,
       native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=_MEAS),
    # --- Load (registers 262-264 are always 0 on a controller with load off) ---
    _s("load_voltage", "Load Voltage", 262, scale=0.1, **_VOLT),
    _s("load_current", "Load Current", 263, scale=0.01,
       suggested_display_precision=2,
       device_class=SensorDeviceClass.CURRENT,
       native_unit_of_measurement=UnitOfElectricCurrent.AMPERE, state_class=_MEAS),
    _s("load_power", "Load Power", 264,
       device_class=SensorDeviceClass.POWER,
       native_unit_of_measurement=UnitOfPower.WATT, state_class=_MEAS),
    # --- PV --------------------------------------------------------------
    _s("pv_voltage", "PV Voltage", 265, scale=0.1, **_VOLT),
    _s("max_charge_power", "Max Charge Power Today", 266,
       device_class=SensorDeviceClass.POWER,
       native_unit_of_measurement=UnitOfPower.WATT, state_class=_MEAS),
    # --- Today -----------------------------------------------------------
    _s("today_charge", "Today Charge", 267,
       device_class=SensorDeviceClass.ENERGY,
       native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
       state_class=SensorStateClass.TOTAL_INCREASING),
    _s("today_discharge", "Today Discharge", 268,
       device_class=SensorDeviceClass.ENERGY,
       native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
       state_class=SensorStateClass.TOTAL_INCREASING),
    _s("battery_voltage_max_today", "Battery Voltage Max Today", 1027, scale=0.1, **_VOLT),
    _s("battery_voltage_min_today", "Battery Voltage Min Today", 1028, scale=0.1, **_VOLT),
    # --- Totals ----------------------------------------------------------
    _s("days", "Running Days", 271, native_unit_of_measurement="d",
       state_class=SensorStateClass.TOTAL_INCREASING),
    _s("total_charge", "Total Charge", 273, scale=0.001,
       suggested_display_precision=2,
       device_class=SensorDeviceClass.ENERGY,
       native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
       state_class=SensorStateClass.TOTAL_INCREASING),
    _s("total_discharge", "Total Discharge", 275, scale=0.001,
       suggested_display_precision=2,
       device_class=SensorDeviceClass.ENERGY,
       native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
       state_class=SensorStateClass.TOTAL_INCREASING),
    # --- Controller information (diagnostic) -----------------------------
    _s("battery_type", "Battery Type",
       value_fn=_opt(lambda r: battery_type_text(r[513]), 513), **_DIAG),
    _s("system_voltage", "System Voltage", REG_SYSTEM_VOLTAGE,
       native_unit_of_measurement="V", **_DIAG),
    _s("charge_stages", "Charge Stages", 515, **_DIAG),
    _s("model", "Model",
       value_fn=_opt(lambda r: ascii_from_registers([r[a] for a in range(12, 19)]) or None,
                     *range(12, 19)), **_DIAG),
    _s("firmware", "Firmware", 11, value_fn=_opt(lambda r: str(r[11]), 11), **_DIAG),
    _s("hardware", "Hardware", 10, value_fn=_opt(lambda r: str(r[10]), 10), **_DIAG),
    # --- Unknown registers, hidden by default (enable to experiment) -----
    _s("status_1", "Status 1 (0x0121)", REG_STATUS_1, **_HIDDEN),
    _s("status_2", "Status 2 (0x0122)", REG_STATUS_2, **_HIDDEN),
    _s("register_269", "Register 0x010D", 269, **_HIDDEN),
    _s("setting_524", "Setting 0x020C", 524, **_HIDDEN),
    _s("setting_525", "Setting 0x020D (timer 1)", 525, **_HIDDEN),
    _s("setting_526", "Setting 0x020E (timer 2)", 526, **_HIDDEN),
    _s("setting_528", "Setting 0x0210 (load)", 528, **_HIDDEN),
    _s("setting_529", "Setting 0x0211 (load max)", 529, **_HIDDEN),
)
