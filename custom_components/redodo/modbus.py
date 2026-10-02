"""Modbus communication layer for Redodo."""

from __future__ import annotations

import asyncio
import inspect

from pymodbus.client import AsyncModbusSerialClient
from pymodbus.framer import FramerType


class RedodoModbus:
    """Thin async wrapper around pymodbus (RTU over RS485)."""

    def __init__(self, port: str, slave: int, baudrate: int) -> None:
        self._slave = slave
        self._client = AsyncModbusSerialClient(
            port=port,
            framer=FramerType.RTU,
            baudrate=baudrate,
            bytesize=8,
            parity="N",
            stopbits=1,
            timeout=1,
        )
        # pymodbus >= 3.10 uses "device_id", older versions use "slave"
        params = inspect.signature(self._client.read_holding_registers).parameters
        self._id_kw = "device_id" if "device_id" in params else "slave"
        self._lock = asyncio.Lock()

    async def connect(self) -> bool:
        if not self._client.connected:
            await self._client.connect()
        return self._client.connected

    async def close(self) -> None:
        if self._client.connected:
            self._client.close()

    async def read_holding_registers(self, address: int, count: int) -> list[int]:
        async with self._lock:
            if not await self.connect():
                raise ConnectionError("Unable to connect")
            result = await self._client.read_holding_registers(
                address=address, count=count, **{self._id_kw: self._slave}
            )
            if result.isError():
                raise RuntimeError(result)
            return list(result.registers)

    async def write_register(self, address: int, value: int) -> None:
        async with self._lock:
            if not await self.connect():
                raise ConnectionError("Unable to connect")
            result = await self._client.write_register(
                address=address, value=value, **{self._id_kw: self._slave}
            )
            if result.isError():
                raise RuntimeError(result)

    async def raw_command(self, frame: bytes) -> None:
        """Send a proprietary frame (functions 0x78 / 0x79).

        pymodbus cannot parse these replies, so the link is closed afterwards;
        the next poll reconnects with clean buffers.
        """
        async with self._lock:
            if not await self.connect():
                raise ConnectionError("Unable to connect")
            # pymodbus >= 3.9 keeps the transport on client.ctx, older on the client
            transport = getattr(getattr(self._client, "ctx", None), "transport", None) or getattr(
                self._client, "transport", None
            )
            if transport is None:
                raise ConnectionError("Serial transport not available")
            transport.write(frame)
            await asyncio.sleep(0.5)
            self._client.close()
