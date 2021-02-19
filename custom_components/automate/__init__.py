"""The Automate Pulse Hub v2 integration."""
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .hub import PulseHub

PLATFORMS = ["cover", "sensor"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Automate Pulse Hub v2 component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Automate Pulse Hub v2 from a config entry."""
    hub = PulseHub(hass, entry)

    if not await hub.async_setup():
        return False

    hass.data[DOMAIN][entry.entry_id] = hub

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hub = hass.data[DOMAIN][entry.entry_id]

    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )

    if not await hub.async_reset():
        return False

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
