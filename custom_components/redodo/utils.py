"""Pure helpers for Redodo (no Home Assistant imports, easy to test)."""

from __future__ import annotations


def modbus_crc(data: bytes) -> bytes:
    """Calculate Modbus RTU CRC16 (low byte first)."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return bytes([crc & 0xFF, (crc >> 8) & 0xFF])


def build_frame(slave: int, function: int, payload: bytes) -> bytes:
    """Build a Modbus RTU frame."""
    frame = bytes([slave, function]) + payload
    return frame + modbus_crc(frame)


def factory_reset_frame(slave: int) -> bytes:
    """Proprietary function 0x78 - factory reset."""
    return build_frame(slave, 0x78, b"\xff\xff\xff\xff")


def clear_history_frame(slave: int) -> bytes:
    """Proprietary function 0x79 - clear energy history."""
    return build_frame(slave, 0x79, b"\xff\xff\xff\xff")


def signed8(value: int) -> int:
    """Interpret a byte as signed (negative temperatures in winter)."""
    value &= 0xFF
    return value - 256 if value > 127 else value


def battery_temp(raw: int) -> int:
    """Low byte of register 261 = battery temperature in deg C."""
    return signed8(raw)


def controller_temp(raw: int) -> int:
    """High byte of register 261 = controller temperature in deg C."""
    return signed8(raw >> 8)


def ascii_from_registers(values: list[int]) -> str:
    """Decode registers holding two ASCII characters each."""
    data = b"".join(v.to_bytes(2, "big") for v in values)
    return data.decode("ascii", errors="ignore").replace("\x00", "").strip()


BATTERY_TYPES = {1: "LiFePO4"}


def battery_type_text(value: int) -> str:
    """Human readable battery type (only 1 = LiFePO4 is confirmed)."""
    return BATTERY_TYPES.get(value, f"Unknown ({value})")
