from __future__ import annotations

from PySide6 import QtWidgets

from qfinancetools.core.plugins import discover_plugins
from qfinancetools.gui.widgets import make_error_banner, make_primary_button, show_error


class PluginsPage(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.error = make_error_banner()
        layout.addWidget(self.error)
        self.table = QtWidgets.QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Version", "Capabilities", "Error"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table, 1)
        layout.addWidget(make_primary_button("Refresh plugins", self._refresh))
        self._refresh()

    def _refresh(self) -> None:
        try:
            snapshot = discover_plugins()
            show_error(self.error, None)
        except Exception as exc:
            show_error(self.error, str(exc))
            return
        self.table.setRowCount(len(snapshot.plugins))
        for row_idx, plugin in enumerate(snapshot.plugins):
            values = [
                plugin.plugin_id,
                plugin.name,
                plugin.version,
                ", ".join(cap.name for cap in plugin.capabilities) if plugin.capabilities else "-",
                plugin.error or "-",
            ]
            for col_idx, value in enumerate(values):
                self.table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(value))
