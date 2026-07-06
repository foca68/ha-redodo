from __future__ import annotations

from homeassistant.const import CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import RedodoCoordinator

PLATFORMS = [
    "sensor",
    "number",
    "select",
    "switch",
    "button",
]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
):

    coordinator = RedodoCoordinator(
        hass,
        port=entry.data[CONF_PORT],
        slave=entry.data["slave"],
        scan_interval=entry.data[CONF_SCAN_INTERVAL],
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True

async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
):

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:

        coordinator = hass.data[DOMAIN].pop(entry.entry_id)

        await coordinator.async_shutdown()

    return unload_ok

