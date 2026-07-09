"""Entity descriptions for Redodo."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.number import NumberDeviceClass
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfCurrent
from homeassistant.const import UnitOfElectricPotential
from homeassistant.const import UnitOfPower
from homeassistant.const import UnitOfTemperature


#
# SENSOR
#

@dataclass(frozen=True)
class RedodoSensorDescription:

    key: str
    name: str
    address: int

    scale: float = 1.0

    unit: str | None = None

    device_class: str | None = None


SENSORS = (

    RedodoSensorDescription(
        "battery_type",
        "Battery Type",
        256,
    ),

    RedodoSensorDescription(
        "battery_soc",
        "Battery SOC",
        257,
        unit="%",
    ),

    RedodoSensorDescription(
        "battery_voltage",
        "Battery Voltage",
        258,
        scale=0.1,
        unit=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),

    RedodoSensorDescription(
        "pv_current",
        "PV Current",
        259,
        scale=0.01,
        unit=UnitOfCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),

    RedodoSensorDescription(
        "pv_power",
        "PV Power",
        260,
        unit=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),

    RedodoSensorDescription(
        "load_current",
        "Load Current",
        261,
        scale=0.1,
        unit=UnitOfCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),

    RedodoSensorDescription(
        "load_power",
        "Load Power",
        262,
        unit=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),

    RedodoSensorDescription(
        "controller_temperature",
        "Controller Temperature",
        263,
        unit=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),

    RedodoSensorDescription(
        "battery_temperature",
        "Battery Temperature",
        264,
        unit=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),

    RedodoSensorDescription(
        "pv_voltage",
        "PV Voltage",
        265,
        scale=0.1,
        unit=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),

    RedodoSensorDescription(
        "max_charge_power",
        "Max Charge Power",
        266,
        unit=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),

    RedodoSensorDescription(
        "today_charge",
        "Today Charge",
        267,
        unit="Wh",
    ),

    RedodoSensorDescription(
        "work_mode",
        "Work Mode",
        270,
    ),

    RedodoSensorDescription(
        "days_counter",
        "Days Counter",
        271,
    ),

    RedodoSensorDescription(
        "error_code",
        "Error Code",
        272,
    ),

    RedodoSensorDescription(
        "total_charge",
        "Total Charge",
        273,
        unit="Wh",
    ),

    RedodoSensorDescription(
        "total_discharge",
        "Total Discharge",
        275,
        unit="Wh",
    ),

    RedodoSensorDescription(
        "freeze_protection",
        "Freeze Protection",
        290,
    ),

    #
    # TODAY
    #

    RedodoSensorDescription(
        "today_load_energy",
        "Today Load Energy",
        1024,
        unit="Wh",
    ),

    RedodoSensorDescription(
        "today_pv_energy",
        "Today PV Energy",
        1025,
        unit="Wh",
    ),

    RedodoSensorDescription(
        "today_peak_power",
        "Today Peak Power",
        1026,
        unit=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),

    RedodoSensorDescription(
        "today_min_battery",
        "Today Min Battery",
        1027,
        scale=0.1,
        unit=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),

    RedodoSensorDescription(
        "today_max_battery",
        "Today Max Battery",
        1028,
        scale=0.1,
        unit=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),

)

#
# NUMBER
#

@dataclass(frozen=True)
class RedodoNumberDescription:

    key: str

    name: str

    address: int

    minimum: float

    maximum: float

    step: float

    scale: float = 1.0

    unit: str | None = None


NUMBERS = (

    RedodoNumberDescription(
        "over_voltage",
        "Over Voltage Protection",
        515,
        10,
        17,
        0.1,
        0.1,
        UnitOfElectricPotential.VOLT,
    ),

    RedodoNumberDescription(
        "equalize_voltage",
        "Equalize Voltage",
        516,
        10,
        15.5,
        0.1,
        0.1,
        UnitOfElectricPotential.VOLT,
    ),

    RedodoNumberDescription(
        "boost_voltage",
        "Boost Voltage",
        517,
        10,
        15.5,
        0.1,
        0.1,
        UnitOfElectricPotential.VOLT,
    ),

    RedodoNumberDescription(
        "float_voltage",
        "Float Voltage",
        518,
        10,
        15,
        0.1,
        0.1,
        UnitOfElectricPotential.VOLT,
    ),

)

#
# SELECT
#

@dataclass(frozen=True)
class RedodoSelectDescription:

    key: str

    name: str

    address: int

    options: dict[int, str]


SELECTS = (

    RedodoSelectDescription(
        key="battery_type",
        name="Battery Type",
        address=513,
        options={
            0: "User",
            1: "Sealed",
            2: "Gel",
            3: "Flooded",
            4: "LiFePO4",
        },
    ),

)

#
# SWITCH
#

@dataclass(frozen=True)
class RedodoSwitchDescription:

    key: str

    name: str

    address: int

    on_value: int = 1

    off_value: int = 0


SWITCHES = (

    RedodoSwitchDescription(
        key="load_output",
        name="Load Output",
        address=288,
    ),

)

#
# BUTTON
#

@dataclass(frozen=True)
class RedodoButtonDescription:

    key: str

    name: str

    address: int

    value: int


BUTTONS = (

    #
    # momentan nu există butoane Modbus simple
    #
    # comenzile speciale din aplicație
    # folosesc frame-uri Modbus complete (0x06 și 0x79)
    # nu un simplu registru.
    #

)