from __future__ import annotations

from PySide6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from qfinancetools.core.afford import affordability
from qfinancetools.models.afford import AffordInput
from qfinancetools.gui.widgets import (
    labeled_field,
    make_error_banner,
    make_form,
    make_primary_button,
    show_error,
    ResultCard,
    annotate_bars,
    apply_chart_theme,
    format_currency_axis,
)


class AffordPage(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        self.income = QtWidgets.QDoubleSpinBox()
        self.income.setRange(0, 1_000_000)
        self.income.setValue(7000)
        self.income.setPrefix("$")
        self.income.setDecimals(2)

        self.debts = QtWidgets.QDoubleSpinBox()
        self.debts.setRange(0, 1_000_000)
        self.debts.setValue(600)
        self.debts.setPrefix("$")
        self.debts.setDecimals(2)

        self.housing = QtWidgets.QDoubleSpinBox()
        self.housing.setRange(0, 1_000_000)
        self.housing.setValue(2200)
        self.housing.setPrefix("$")
        self.housing.setDecimals(2)

        self.max_dti = QtWidgets.QDoubleSpinBox()
        self.max_dti.setRange(0.01, 1)
        self.max_dti.setValue(0.36)
        self.max_dti.setSingleStep(0.01)
        self.max_dti.setDecimals(3)

        self.stress_rate = QtWidgets.QDoubleSpinBox()
        self.stress_rate.setRange(0, 100)
        self.stress_rate.setValue(2)
        self.stress_rate.setSuffix("%")
        self.stress_rate.setDecimals(2)

        form = make_form(
            [
                labeled_field("Monthly income", self.income),
                labeled_field("Monthly debts", self.debts),
                labeled_field("Housing cost", self.housing),
                labeled_field("Max DTI", self.max_dti),
                labeled_field("Stress rate", self.stress_rate),
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

        self.card_allowed = ResultCard("Max housing", "$0")
        self.card_current = ResultCard("Current DTI", "0%")
        self.card_stressed = ResultCard("Stressed DTI", "0%")
        self.card_afford = ResultCard("Affordable", "No")
        cards = QtWidgets.QHBoxLayout()
        cards.addWidget(self.card_allowed)
        cards.addWidget(self.card_current)
        cards.addWidget(self.card_stressed)
        cards.addWidget(self.card_afford)
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
            data = AffordInput(
                income_monthly=self.income.value(),
                debts_monthly=self.debts.value(),
                housing_cost=self.housing.value(),
                max_dti=self.max_dti.value(),
                stress_rate=self.stress_rate.value(),
            )
            result = affordability(data)
            show_error(self.error_banner, None)
        except Exception as exc:
            show_error(self.error_banner, str(exc))
            return

        self.card_allowed.set_value(f"${result.allowed_housing:,.2f}")
        self.card_current.set_value(f"{result.current_dti * 100:.2f}%")
        self.card_stressed.set_value(f"{result.stressed_dti * 100:.2f}%")
        self.card_afford.set_value("Yes" if result.affordable else "No")
        self._render_chart(result)

    def _render_chart(self, result) -> None:
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        stressed_housing = self.housing.value() * (1 + self.stress_rate.value() / 100)
        values = [self.housing.value(), result.allowed_housing, stressed_housing]
        labels = ["Current", "Max", "Stressed"]
        colors = ["#94a3b8", "#0ea5e9", "#38bdf8"]
        ax.bar(labels, values, color=colors)
        ax.set_ylabel("Monthly")
        apply_chart_theme(ax)
        format_currency_axis(ax, "y")
        annotate_bars(ax, fmt="${:,.0f}")
        self.figure.tight_layout()
        self.canvas.draw()
