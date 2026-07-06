import logging
import struct
from typing import List

import serial

from .const import (
    DEFAULT_BAUDRATE,
    DEFAULT_BYTESIZE,
    DEFAULT_PARITY,
    DEFAULT_STOPBITS,
    DEFAULT_TIMEOUT,
)

_LOGGER = logging.getLogger(__name__)

class RedodoModbus:
    """Redodo native Modbus RTU driver."""

    def __init__(
        self,
        port: str,
        slave: int = 1,
        baudrate: int = DEFAULT_BAUDRATE,
        timeout: float = DEFAULT_TIMEOUT,
    ):

        self._slave = slave

        self._serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=DEFAULT_BYTESIZE,
            parity=DEFAULT_PARITY,
            stopbits=DEFAULT_STOPBITS,
            timeout=timeout,
        )

    @staticmethod
    def crc16(data: bytes) -> bytes:
        crc = 0xFFFF

        for byte in data:
            crc ^= byte

            for _ in range(8):
                if crc & 1:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1

        return struct.pack("<H", crc)

    def _send(self, frame: bytes) -> bytes:

        packet = frame + self.crc16(frame)

        _LOGGER.debug("TX %s", packet.hex(" "))

        self._serial.reset_input_buffer()
        self._serial.write(packet)
        self._serial.flush()

        response = self._serial.read(256)

        _LOGGER.debug("RX %s", response.hex(" "))

        return response

    def read_registers(
        self,
        start: int,
        count: int,
    ) -> List[int]:

        frame = struct.pack(
            ">BBHH",
            self._slave,
            0x03,
            start,
            count,
        )

        response = self._send(frame)

        if len(response) < 5:
            raise RuntimeError("No response")

        payload = response[:-2]

        crc = response[-2:]

        if crc != self.crc16(payload):
            raise RuntimeError("CRC error")

        if response[1] != 0x03:
            raise RuntimeError("Invalid response")

        bytecount = response[2]

        values = []

        for i in range(0, bytecount, 2):

            value = struct.unpack(
                ">H",
                response[3 + i:5 + i],
            )[0]

            values.append(value)

        return values

    def read_home(self):

        return self.read_registers(
            0x0101,
            19,
        )

    def read_settings(self):

        return self.read_registers(
            0x0201,
            17,
        )

    def read_today(self):

        return self.read_registers(
            0x0400,
            5,
        )

    def write_single(
        self,
        register: int,
        value: int,
    ) -> bool:

        frame = struct.pack(
            ">BBHH",
            self._slave,
            0x06,
            register,
            value,
        )

        response = self._send(frame)

        if len(response) != 8:
            return False

        return response == frame + self.crc16(frame)

    def write_multiple(
        self,
        start: int,
        values: list[int],
    ) -> bool:

        quantity = len(values)

        frame = bytearray()

        frame.append(self._slave)
        frame.append(0x10)

        frame.extend(struct.pack(">H", start))
        frame.extend(struct.pack(">H", quantity))

        frame.append(quantity * 2)

        for value in values:
            frame.extend(struct.pack(">H", value))

        response = self._send(bytes(frame))

        if len(response) != 8:
            return False

        payload = response[:-2]

        if response[-2:] != self.crc16(payload):
            return False

        return True

    def close(self):

        if self._serial.is_open:
            self._serial.close()

