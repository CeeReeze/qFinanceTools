from __future__ import annotations

from PySide6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from qfinancetools.core.investments import investment_growth
from qfinancetools.models.investments import InvestmentInput
from qfinancetools.gui.widgets import (
    labeled_field,
    make_error_banner,
    make_form,
    make_primary_button,
    show_error,
    ResultCard,
    apply_chart_theme,
    format_currency_axis,
    annotate_bars,
)


class InvestPage(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        self.initial = QtWidgets.QDoubleSpinBox()
        self.initial.setRange(0, 1_000_000_000)
        self.initial.setValue(10000)
        self.initial.setPrefix("$")
        self.initial.setDecimals(2)

        self.monthly = QtWidgets.QDoubleSpinBox()
        self.monthly.setRange(0, 1_000_000)
        self.monthly.setValue(500)
        self.monthly.setPrefix("$")
        self.monthly.setDecimals(2)

        self.rate = QtWidgets.QDoubleSpinBox()
        self.rate.setRange(0, 100)
        self.rate.setValue(7)
        self.rate.setSuffix("%")
        self.rate.setDecimals(3)

        self.years = QtWidgets.QSpinBox()
        self.years.setRange(1, 100)
        self.years.setValue(20)

        form = make_form(
            [
                labeled_field("Initial", self.initial),
                labeled_field("Monthly contribution", self.monthly),
                labeled_field("Annual rate", self.rate),
                labeled_field("Horizon (years)", self.years),
            ]
        )

        left = QtWidgets.QVBoxLayout()
        left.addWidget(form)
        left.addStretch(1)
        left.addWidget(make_primary_button("Calculate", self._calculate))
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)

        right = QtWidgets.QVBoxLayout()
        self.error_banner = make_error_banner()
        right.addWidget(self.error_banner)

        self.card_final = ResultCard("Final value", "$0")
        self.card_contrib = ResultCard("Total contributions", "$0")
        self.card_growth = ResultCard("Total growth", "$0")
        cards = QtWidgets.QHBoxLayout()
        cards.addWidget(self.card_final)
        cards.addWidget(self.card_contrib)
        cards.addWidget(self.card_growth)
        right.addLayout(cards)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(240)
        right.addWidget(self.canvas, 2)
        right.addStretch(1)

        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([320, 800])
        layout.addWidget(splitter)

        self._calculate()

    def _calculate(self) -> None:
        try:
            data = InvestmentInput(
                initial=self.initial.value(),
                monthly=self.monthly.value(),
                annual_rate=self.rate.value(),
                years=self.years.value(),
            )
            result = investment_growth(data)
            show_error(self.error_banner, None)
        except Exception as exc:
            show_error(self.error_banner, str(exc))
            return

        self.card_final.set_value(f"${result.final_value:,.2f}")
        self.card_contrib.set_value(f"${result.total_contributions:,.2f}")
        self.card_growth.set_value(f"${result.total_growth:,.2f}")
        self._render_chart(result.total_contributions, result.total_growth)

    def _render_chart(self, contributions: float, growth: float) -> None:
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        bars = ax.bar(["Contributions", "Growth"], [contributions, growth], color=["#94a3b8", "#0ea5e9"])
        total = contributions + growth
        ax.text(0.5, max(contributions, growth) * 1.08, f"Total ${total:,.0f}", ha="center", va="bottom", fontsize=9)
        ax.set_ylabel("Value")
        apply_chart_theme(ax)
        format_currency_axis(ax, "y")
        annotate_bars(ax, fmt="${:,.0f}")
        self.figure.tight_layout()
        self.canvas.draw()
