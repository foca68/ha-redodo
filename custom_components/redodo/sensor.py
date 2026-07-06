from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
)

from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfEnergy,
    PERCENTAGE,
)

from .const import DOMAIN
from .entity import RedodoEntity


@dataclass
class RedodoSensorDescription(SensorEntityDescription):
    table: str = "home"
    index: int = 0
    scale: float = 1.0


SENSORS = (

    RedodoSensorDescription(
        key="battery_type",
        name="Battery Type",
        index=0,
    ),

    RedodoSensorDescription(
        key="battery_soc",
        name="Battery SOC",
        index=1,
        native_unit_of_measurement=PERCENTAGE,
    ),

    RedodoSensorDescription(
        key="battery_voltage",
        name="Battery Voltage",
        index=2,
        scale=0.1,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),

    RedodoSensorDescription(
        key="pv_current",
        name="PV Current",
        index=3,
        scale=0.01,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),

    RedodoSensorDescription(
        key="pv_power",
        name="PV Power",
        index=4,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),

    RedodoSensorDescription(
        key="load_current",
        name="Load Current",
        index=5,
        scale=0.1,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),

    RedodoSensorDescription(
        key="load_power",
        name="Load Power",
        index=6,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),

    RedodoSensorDescription(
        key="controller_temperature",
        name="Controller Temperature",
        index=7,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),

    RedodoSensorDescription(
        key="battery_temperature",
        name="Battery Temperature",
        index=8,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),

    RedodoSensorDescription(
        key="pv_voltage",
        name="PV Voltage",
        index=9,
        scale=0.1,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),

    RedodoSensorDescription(
        key="max_charge_power",
        name="Max Charge Power",
        index=10,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),

    RedodoSensorDescription(
        key="charge_today",
        name="Charge Today",
        index=11,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),

    RedodoSensorDescription(
        key="work_mode",
        name="Work Mode",
        index=14,
    ),

    RedodoSensorDescription(
        key="days",
        name="Days",
        index=15,
    ),

    RedodoSensorDescription(
        key="error_code",
        name="Error Code",
        index=16,
    ),

    RedodoSensorDescription(
        key="total_charge",
        name="Total Charge",
        index=17,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),

    RedodoSensorDescription(
        key="total_discharge",
        name="Total Discharge",
        index=19,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),

    RedodoSensorDescription(
        key="freeze_protection",
        name="Freeze Protection",
        index=34,
    ),

    #
    # TODAY DATA
    #

    RedodoSensorDescription(
        key="today_load_energy",
        name="Today Load Energy",
        table="today",
        index=0,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),

    RedodoSensorDescription(
        key="today_charge_energy",
        name="Today Charge Energy",
        table="today",
        index=1,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),

    RedodoSensorDescription(
        key="today_peak_power",
        name="Today Peak Power",
        table="today",
        index=2,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),

    RedodoSensorDescription(
        key="today_battery_min",
        name="Today Battery Min",
        table="today",
        index=3,
        scale=0.1,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),

    RedodoSensorDescription(
        key="today_battery_max",
        name="Today Battery Max",
        table="today",
        index=4,
        scale=0.1,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),

)

class RedodoSensor(RedodoEntity, SensorEntity):

    entity_description: RedodoSensorDescription

    def __init__(self, coordinator, description):
        super().__init__(
            coordinator,
            description.name,
            description.key,
        )

        self.entity_description = description

    @property
    def native_value(self):

        if self.entity_description.table == "home":
            value = self.coordinator.get_home(
                self.entity_description.index
            )
        else:
            value = self.coordinator.get_today(
                self.entity_description.index
            )

        if self.entity_description.scale != 1:
            value = value * self.entity_description.scale

        return value

async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        RedodoSensor(
            coordinator,
            description,
        )
        for description in SENSORS
    )

