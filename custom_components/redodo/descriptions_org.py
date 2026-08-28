"""Entity descriptions for Redodo."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfTemperature,
)


@dataclass(frozen=True, kw_only=True)
class RedodoSensorDescription(SensorEntityDescription):
    """Redodo sensor description."""

    address: int = 0
    scale: float = 1.0


SENSORS = (

    # RedodoSensorDescription(
        # key="battery_type",
        # name="Battery Type-V",
        # address=256,
    # ),

    RedodoSensorDescription(
        key="battery_soc",
        name="Battery SOC",
        address=257,
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
    ),

    RedodoSensorDescription(
        key="battery_voltage",
        name="Battery Voltage",
        address=258,
        scale=0.1,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    RedodoSensorDescription(
        key="pv_current",
        name="PV Current",
        address=259,
        scale=0.01,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    RedodoSensorDescription(
        key="pv_power",
        name="PV Power",
        address=260,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    RedodoSensorDescription(
        key="load_current",
        name="Load Current",
        address=263, #261 nedectat
        scale=0.01,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    RedodoSensorDescription(
        key="load_power",
        name="Load Power",
        address=264, #262 tensiune iesire MPPT sau Battery Bank Voltage
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    # RedodoSensorDescription(
        # key="controller_temperature",
        # name="Controller Temperature",
        # address=263, #Load Current
        # device_class=SensorDeviceClass.TEMPERATURE,
        # native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        # state_class=SensorStateClass.MEASUREMENT,
    # ),

    # RedodoSensorDescription(
        # key="battery_temperature",
        # name="Battery Temperature",
        # address=264, #Load Power
        # device_class=SensorDeviceClass.TEMPERATURE,
        # native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        # state_class=SensorStateClass.MEASUREMENT,
    # ),

    RedodoSensorDescription(
        key="pv_voltage",
        name="PV Voltage",
        address=265,
        scale=0.1,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    RedodoSensorDescription(
        key="max_charge_power",
        name="Max Charge Power",
        address=266,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    RedodoSensorDescription(
        key="today_charge",
        name="Today Charge",
        address=267,
        native_unit_of_measurement="Wh",
    ),

    # RedodoSensorDescription(
        # key="work_mode",
        # name="Work Mode",
        # address=270,
    # ),

    RedodoSensorDescription(
        key="days",
        name="Days",
        address=271,
    ),

    # RedodoSensorDescription(
        # key="error_code",
        # name="Error Code",
        # address=272,
    # ),

    RedodoSensorDescription(
        key="total_charge",
        name="Total Charge",
        address=273,
        native_unit_of_measurement="Wh",
    ),

    RedodoSensorDescription(
        key="total_discharge",
        name="Total Discharge",
        address=275,
        native_unit_of_measurement="Wh",
    ),

    # RedodoSensorDescription(
        # key="low_temp_status",
        # name="Low Temperature Protection",
        # address=290,
    # ),

    # RedodoSensorDescription(
        # key="today_load_energy",
        # name="Today's Load Energy",
        # address=1024,
        # native_unit_of_measurement="Wh",
    # ),

    RedodoSensorDescription(
        key="today_discharge_energy",
        name="Today's Discharge Energy",
        address=1025,
        native_unit_of_measurement="Wh",
    ),

    RedodoSensorDescription(
        key="today_peak_power",
        name="Today's Peak Power",
        address=1026,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),

    # RedodoSensorDescription(
        # key="today_min_voltage",
        # name="Today's Min Battery Voltage",
        # address=1027,
        # scale=0.2,
        # device_class=SensorDeviceClass.VOLTAGE,
        # native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    # ),

    # RedodoSensorDescription(
        # key="today_max_voltage",
        # name="Today's Max Battery Voltage",
        # address=1028,
        # scale=0.2,
        # device_class=SensorDeviceClass.VOLTAGE,
        # native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    # ),

)