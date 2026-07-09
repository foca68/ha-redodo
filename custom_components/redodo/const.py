DOMAIN = "redodo"

NAME = "Redodo MPPT"

MANUFACTURER = "Redodo"

DEFAULT_SLAVE = 1

DEFAULT_BAUDRATE = 9600

DEFAULT_BYTESIZE = 8

DEFAULT_PARITY = "N"

DEFAULT_STOPBITS = 1

DEFAULT_TIMEOUT = 1.0

DEFAULT_SCAN_INTERVAL = 5

FUNCTION_READ = 0x03
FUNCTION_WRITE_SINGLE = 0x06
FUNCTION_WRITE_MULTI = 0x10

    def read_home(self):
        return self.read_registers(
            READ_HOME_START,
            READ_HOME_COUNT,
        )

    def read_settings(self):
        return self.read_registers(
            READ_SETTINGS_START,
            READ_SETTINGS_COUNT,
        )

    def read_today(self):
        return self.read_registers(
            READ_TODAY_START,
            READ_TODAY_COUNT,
        )

from .const import (
    DEFAULT_BAUDRATE,
    DEFAULT_BYTESIZE,
    DEFAULT_PARITY,
    DEFAULT_STOPBITS,
    DEFAULT_TIMEOUT,
    READ_HOME_START,
    READ_HOME_COUNT,
    READ_SETTINGS_START,
    READ_SETTINGS_COUNT,
    READ_TODAY_START,
    READ_TODAY_COUNT,
)