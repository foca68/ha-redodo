"""Constants for Redodo integration."""

DOMAIN = "redodo"

DEFAULT_NAME = "Redodo"
DEFAULT_SLAVE = 1
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 9600
DEFAULT_SCAN_INTERVAL = 5  # seconds

CONF_SLAVE = "slave"
CONF_BAUDRATE = "baudrate"
CONF_SCAN_INTERVAL = "scan_interval"

# Register blocks (decimal Modbus holding-register addresses)
LIVE_START = 256  # 0x0100
LIVE_COUNT = 35  # 256..290
SETTING_START = 512  # 0x0200
SETTING_COUNT = 18  # 512..529
TODAY_START = 1024  # 0x0400
TODAY_COUNT = 5  # 1024..1028
INFO_START = 10  # 0x000A
INFO_COUNT = 16  # 10..25

# Settings and device info change rarely: refresh them every N live polls
SETTINGS_EVERY = 6

# Individual registers
REG_TEMPS = 261  # high byte = controller temp, low byte = battery temp (deg C)
REG_LOAD_SWITCH = 288  # 0x0120
REG_FORCE_CHARGE = 289  # 0x0121
REG_STATUS_1 = 289
REG_STATUS_2 = 290
REG_SYSTEM_VOLTAGE = 514
