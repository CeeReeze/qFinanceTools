from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from PySide6 import QtCore, QtGui, QtWidgets
from matplotlib.ticker import FuncFormatter


@dataclass(frozen=True)
class FieldSpec:
    label: str
    widget: QtWidgets.QWidget


def parse_list_floats(raw: str) -> list[float]:
    text = raw.strip()
    if not text:
        return []
    parts = [p for p in text.replace(",", " ").split() if p]
    return [float(p) for p in parts]


def parse_list_ints(raw: str) -> list[int]:
    text = raw.strip()
    if not text:
        return []
    parts = [p for p in text.replace(",", " ").split() if p]
    return [int(p) for p in parts]


def labeled_field(label: str, widget: QtWidgets.QWidget) -> FieldSpec:
    return FieldSpec(label=label, widget=widget)


def make_form(fields: list[FieldSpec]) -> QtWidgets.QWidget:
    form = QtWidgets.QWidget()
    layout = QtWidgets.QFormLayout(form)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(10)
    for field in fields:
        layout.addRow(field.label, field.widget)
    return form


def make_primary_button(text: str, on_click: Callable[[], None]) -> QtWidgets.QPushButton:
    btn = QtWidgets.QPushButton(text)
    btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    btn.clicked.connect(on_click)
    btn.setDefault(True)
    return btn


def make_error_banner() -> QtWidgets.QLabel:
    label = QtWidgets.QLabel("")
    label.setObjectName("ErrorBanner")
    label.setWordWrap(True)
    label.hide()
    return label


def show_error(label: QtWidgets.QLabel, message: str | None) -> None:
    if message:
        label.setText(message)
        label.show()
    else:
        label.setText("")
        label.hide()


class ResultCard(QtWidgets.QFrame):
    def __init__(self, title: str, value: str) -> None:
        super().__init__()
        self.setObjectName("ResultCard")
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(4)
        title_label = QtWidgets.QLabel(title)
        title_label.setObjectName("ResultCardTitle")
        value_label = QtWidgets.QLabel(value)
        value_label.setObjectName("ResultCardValue")
        layout.addWidget(title_label)
        layout.addWidget(value_label)

    def set_value(self, value: str) -> None:
        label = self.findChild(QtWidgets.QLabel, "ResultCardValue")
        if label is not None:
            label.setText(value)


def style_axes(ax) -> None:
    ax.grid(True, axis="y", color="#e2e8f0", linewidth=1, alpha=0.8)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#cbd5e1")
    ax.spines["bottom"].set_color("#cbd5e1")
    ax.tick_params(axis="both", labelsize=9, colors="#334155")
    ax.set_facecolor("#f8fafc")


def apply_chart_theme(ax, title: str | None = None) -> None:
    if title:
        ax.set_title(title, fontsize=10, color="#0f172a", pad=8)
    style_axes(ax)


def format_currency_axis(ax, axis: str = "y") -> None:
    formatter = FuncFormatter(lambda x, _: f"${x:,.0f}")
    if axis == "x":
        ax.xaxis.set_major_formatter(formatter)
    else:
        ax.yaxis.set_major_formatter(formatter)


def format_percent_axis(ax, axis: str = "y") -> None:
    formatter = FuncFormatter(lambda x, _: f"{x:.0f}%")
    if axis == "x":
        ax.xaxis.set_major_formatter(formatter)
    else:
        ax.yaxis.set_major_formatter(formatter)


def annotate_bars(ax, fmt: str = "{:,.0f}") -> None:
    for bar in ax.patches:
        height = bar.get_height()
        ax.annotate(
            fmt.format(height),
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#0f172a",
        )
