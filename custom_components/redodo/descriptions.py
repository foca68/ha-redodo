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
    is_fahrenheit: bool = False  # Adăugăm această linie nouă

SENSORS = (

    RedodoSensorDescription(
        key="battery_type",
        name="Battery Type",
        address=256, #registru corect
    ),

    RedodoSensorDescription(
        key="battery_soc",
        name="Battery SOC",
        address=257, #registru corect
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
    ),

    RedodoSensorDescription(
        key="battery_voltage",
        name="Battery Voltage",
        address=258, #registru corect
        scale=0.1,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    
        RedodoSensorDescription(
        key="pv_voltage",
        name="PV Voltage",
        address=265, #registru corect  
        scale=0.1,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    
    RedodoSensorDescription(
        key="charge_current",
        name="Charge Current",
        address=259, #registru corect  
        scale=0.01,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
 
    RedodoSensorDescription(
        key="charge_power",
        name="Charge Power",
        address=260, #registru corect
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),  
    
    RedodoSensorDescription(
        key="charge_voltage",
        name="Charge Voltage",
        address=262, #registru corect
        scale=0.1,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    
    RedodoSensorDescription(
        key="load_voltage",
        name="Load Voltage",
        address=262,  # ??
        scale=0.1,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    RedodoSensorDescription(
        key="load_current",
        name="Load Current",
        address=263, #registru corect
        scale=0.01,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    RedodoSensorDescription(
        key="load_power",
        name="Load Power",
        address=264, #registru corect
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),


    RedodoSensorDescription(
        key="max_charge_power",
        name="Max Charge Power",
        address=266, #registru corect
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    RedodoSensorDescription(
        key="today_charge",
        name="Today Charge",
        address=267, #registru corect
        native_unit_of_measurement="Wh",
    ),
    
    RedodoSensorDescription(
        key="today_discharge",
        name="Today Discharge",
        address=268, #registru corect
        native_unit_of_measurement="Wh",
    ),


# În interiorul listei SENSORS:
    # RedodoSensorDescription(  # structura incorecta
        # key="battery_temperature",
        # name="Battery Temperature",
        # address=269,
        # scale=0.1,
        # is_fahrenheit=True,
        # device_class=SensorDeviceClass.TEMPERATURE,
        # native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        # state_class=SensorStateClass.MEASUREMENT,
    # ),



    RedodoSensorDescription(
        key="days",
        name="Days",
        address=271,
    ),



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
        # key="work_mode",
        # name="Work Mode",
        # address=270,
    # ),
    
    # RedodoSensorDescription(
        # key="error_code",
        # name="Error Code",
        # address=272,
    # ),
)
