"""Diagnostics: download the raw register dump from the device page."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict:
    c = hass.data[DOMAIN][entry.entry_id]
    regs = c.data or {}
    return {
        "entry": dict(entry.data),
        "options": dict(entry.options),
        "model": c.model,
        "hardware": c.hw_version,
        "firmware": c.sw_version,
        "registers_dec": {str(k): v for k, v in sorted(regs.items())},
        "registers_hex": {f"0x{k:04X}": f"0x{v:04X}" for k, v in sorted(regs.items())},
    }
