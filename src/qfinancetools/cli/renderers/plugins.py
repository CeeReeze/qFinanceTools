from __future__ import annotations

from rich.console import Console
from rich.table import Table

from qfinancetools.models.plugins import PluginRegistrySnapshot


def render_plugins(snapshot: PluginRegistrySnapshot) -> None:
    table = Table(title="Discovered Plugins")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Version")
    table.add_column("Capabilities")
    table.add_column("Error")

    for plugin in snapshot.plugins:
        caps = ", ".join(item.name for item in plugin.capabilities) if plugin.capabilities else "-"
        table.add_row(plugin.plugin_id, plugin.name, plugin.version, caps, plugin.error or "-")
    Console().print(table)
