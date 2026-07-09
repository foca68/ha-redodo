"""Modbus communication layer for Redodo."""

from __future__ import annotations

import asyncio
import logging

from pymodbus.client import AsyncModbusSerialClient

_LOGGER = logging.getLogger(__name__)


class RedodoModbus:

    def __init__(
        self,
        port: str,
        slave: int,
        baudrate: int,
    ):

        self._slave = slave

        self._client = AsyncModbusSerialClient(
            port=port,
            baudrate=baudrate,
            bytesize=8,
            parity="N",
            stopbits=1,
            timeout=1,
        )

        self._lock = asyncio.Lock()

    async def connect(self):

        if not self._client.connected:
            await self._client.connect()

        return self._client.connected

    async def close(self):

        if self._client.connected:
            self._client.close()

    async def read_holding_registers(
        self,
        address: int,
        count: int,
    ):

        async with self._lock:

            if not await self.connect():
                raise ConnectionError("Unable to connect")

            result = await self._client.read_holding_registers(
                address=address,
                count=count,
                device_id=self._slave,
            )

            if result.isError():
                raise RuntimeError(result)

            return result.registers

    async def write_register(
        self,
        address: int,
        value: int,
    ):

        async with self._lock:

            if not await self.connect():
                raise ConnectionError("Unable to connect")

            result = await self._client.write_register(
                address=address,
                value=value,
                device_id=self._slave,
            )

            if result.isError():
                raise RuntimeError(result)

            return True

    async def write_registers(
        self,
        address: int,
        values: list[int],
    ):

        async with self._lock:

            if not await self.connect():
                raise ConnectionError("Unable to connect")

            result = await self._client.write_registers(
                address=address,
                values=values,
                device_id=self._slave,
            )

            if result.isError():
                raise RuntimeError(result)

            return True