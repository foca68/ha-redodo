"""Utilities for Redodo."""

from __future__ import annotations


def modbus_crc(data: bytes) -> bytes:
    """Calculate Modbus RTU CRC16."""

    crc = 0xFFFF

    for byte in data:

        crc ^= byte

        for _ in range(8):

            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1

    return bytes(
        [
            crc & 0xFF,
            (crc >> 8) & 0xFF,
        ]
    )


def build_frame(
    slave: int,
    function: int,
    payload: bytes,
) -> bytes:
    """Build Modbus RTU frame."""

    frame = bytes(
        [
            slave,
            function,
        ]
    ) + payload

    return frame + modbus_crc(frame)


def factory_reset_frame(
    slave: int,
) -> bytes:

    return build_frame(
        slave,
        0x78,
        b"\xFF\xFF\xFF\xFF",
    )


def clear_history_frame(
    slave: int,
) -> bytes:

    return build_frame(
        slave,
        0x79,
        b"\xFF\xFF\xFF\xFF",
    )


def force_charge_frame(
    slave: int,
    enable: bool,
) -> bytes:

    value = 0x01FF if enable else 0x0000

    payload = bytes(
        [
            0x01,
            0x21,
            (value >> 8) & 0xFF,
            value & 0xFF,
        ]
    )

    return build_frame(
        slave,
        0x06,
        payload,
    )


def low_temperature_frame(
    slave: int,
    enable: bool,
) -> bytes:

    value = 0x0001 if enable else 0x0000

    payload = bytes(
        [
            0x01,
            0x22,
            (value >> 8) & 0xFF,
            value & 0xFF,
        ]
    )

    return build_frame(
        slave,
        0x06,
        payload,
    )