from __future__ import annotations

import importlib.metadata

from qfinancetools.models.plugins import PluginCapability, PluginMeta, PluginRegistrySnapshot


def discover_plugins() -> PluginRegistrySnapshot:
    plugins: list[PluginMeta] = []
    entry_points = importlib.metadata.entry_points(group="qfinance.plugins")
    for entry_point in entry_points:
        try:
            loaded = entry_point.load()
            plugin = loaded() if callable(loaded) else loaded
            capabilities_raw = getattr(plugin, "capabilities", [])
            capabilities = [
                PluginCapability(
                    name=str(item.get("name", "unknown")),
                    description=str(item.get("description", "")),
                )
                if isinstance(item, dict)
                else PluginCapability(name=str(item), description="")
                for item in capabilities_raw
            ]
            plugins.append(
                PluginMeta(
                    plugin_id=str(getattr(plugin, "id", entry_point.name)),
                    name=str(getattr(plugin, "name", entry_point.name)),
                    version=str(getattr(plugin, "version", "unknown")),
                    capabilities=capabilities,
                )
            )
        except Exception as exc:
            plugins.append(
                PluginMeta(
                    plugin_id=entry_point.name,
                    name=entry_point.name,
                    version="unknown",
                    capabilities=[],
                    error=str(exc),
                )
            )
    return PluginRegistrySnapshot(plugins=plugins)
