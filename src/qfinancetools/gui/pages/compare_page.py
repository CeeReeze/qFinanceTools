from __future__ import annotations

from PySide6 import QtWidgets

from qfinancetools.core.comparison import compare_scenarios
from qfinancetools.models.comparison import ComparisonCase, ComparisonRequest
from qfinancetools.gui.widgets import make_error_banner, make_primary_button, show_error


class ComparePage(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self._loan_tab(), "Loan")
        tabs.addTab(self._invest_tab(), "Invest")
        tabs.addTab(self._risk_tab(), "Risk")
        layout.addWidget(tabs)

    def _loan_tab(self) -> QtWidgets.QWidget:
        return _comparison_tab(
            "loan",
            [("amount", 350000.0), ("rate", 5.4), ("years", 25.0), ("extra", 0.0)],
            [("amount", 350000.0), ("rate", 4.8), ("years", 20.0), ("extra", 100.0)],
        )

    def _invest_tab(self) -> QtWidgets.QWidget:
        return _comparison_tab(
            "invest",
            [("initial", 10000.0), ("monthly", 500.0), ("rate", 7.0), ("years", 20.0)],
            [("initial", 10000.0), ("monthly", 700.0), ("rate", 8.0), ("years", 20.0)],
        )

    def _risk_tab(self) -> QtWidgets.QWidget:
        return _comparison_tab(
            "risk",
            [("initial", 10000.0), ("mean", 7.0), ("volatility", 15.0), ("years", 20.0), ("sims", 1000.0), ("seed", 42.0)],
            [("initial", 10000.0), ("mean", 8.0), ("volatility", 18.0), ("years", 20.0), ("sims", 1000.0), ("seed", 42.0)],
        )


def _comparison_tab(
    calculator: str,
    base_defaults: list[tuple[str, float]],
    alt_defaults: list[tuple[str, float]],
) -> QtWidgets.QWidget:
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(widget)
    top = QtWidgets.QHBoxLayout()

    base_form = QtWidgets.QFormLayout()
    alt_form = QtWidgets.QFormLayout()
    base_inputs: dict[str, QtWidgets.QDoubleSpinBox] = {}
    alt_inputs: dict[str, QtWidgets.QDoubleSpinBox] = {}

    for key, value in base_defaults:
        box = QtWidgets.QDoubleSpinBox()
        box.setRange(0, 1_000_000_000)
        box.setDecimals(4)
        box.setValue(value)
        base_form.addRow(f"Base {key}", box)
        base_inputs[key] = box
    for key, value in alt_defaults:
        box = QtWidgets.QDoubleSpinBox()
        box.setRange(0, 1_000_000_000)
        box.setDecimals(4)
        box.setValue(value)
        alt_form.addRow(f"Alt {key}", box)
        alt_inputs[key] = box

    base_box = QtWidgets.QGroupBox("Base Case")
    base_box.setLayout(base_form)
    alt_box = QtWidgets.QGroupBox("Alt Case")
    alt_box.setLayout(alt_form)
    top.addWidget(base_box)
    top.addWidget(alt_box)
    layout.addLayout(top)

    error = make_error_banner()
    layout.addWidget(error)
    table = QtWidgets.QTableWidget(0, 5)
    table.setHorizontalHeaderLabels(["Metric", "Base", "Alt", "Delta", "Delta %"])
    table.horizontalHeader().setStretchLastSection(True)
    layout.addWidget(table, 1)

    def calculate() -> None:
        try:
            base_inputs_raw = {
                key: int(box.value()) if key in ("years", "sims", "seed") else float(box.value())
                for key, box in base_inputs.items()
            }
            alt_inputs_raw = {
                key: int(box.value()) if key in ("years", "sims", "seed") else float(box.value())
                for key, box in alt_inputs.items()
            }
            request = ComparisonRequest(
                calculator=calculator,
                base=ComparisonCase(label="Base", inputs=base_inputs_raw),
                alt=ComparisonCase(label="Alt", inputs=alt_inputs_raw),
            )
            result = compare_scenarios(request)
            show_error(error, None)
        except Exception as exc:
            show_error(error, str(exc))
            return

        table.setRowCount(len(result.deltas))
        for row_idx, delta in enumerate(result.deltas):
            values = [
                delta.metric,
                f"{delta.base_value:,.2f}",
                f"{delta.alt_value:,.2f}",
                f"{delta.absolute_delta:,.2f}",
                f"{delta.percent_delta:,.2f}%" if delta.percent_delta is not None else (delta.percent_delta_reason or "n/a"),
            ]
            for col_idx, value in enumerate(values):
                table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(value))

    layout.addWidget(make_primary_button("Compare", calculate))
    calculate()
    return widget
