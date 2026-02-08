from __future__ import annotations

from PySide6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from qfinancetools.core.risk import scenario, sensitivity, monte_carlo, stress_test
from qfinancetools.models.risk import (
    ScenarioInput,
    SensitivityInput,
    MonteCarloInput,
    StressTestInput,
)
from qfinancetools.gui.widgets import (
    labeled_field,
    make_error_banner,
    make_form,
    make_primary_button,
    show_error,
    ResultCard,
    parse_list_floats,
    annotate_bars,
    apply_chart_theme,
    format_currency_axis,
)


class RiskPage(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self._build_scenario_tab(), "Scenario")
        tabs.addTab(self._build_sensitivity_tab(), "Sensitivity")
        tabs.addTab(self._build_monte_tab(), "Monte Carlo")
        tabs.addTab(self._build_stress_tab(), "Stress Test")
        layout.addWidget(tabs)

    def _build_scenario_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        base = QtWidgets.QDoubleSpinBox()
        base.setRange(0, 1_000_000_000)
        base.setValue(10000)

        shocks = QtWidgets.QLineEdit("-10, 0, 10, 20")

        form = make_form(
            [
                labeled_field("Base value", base),
                labeled_field("Shocks (%)", shocks),
            ]
        )

        left = QtWidgets.QVBoxLayout()
        left.addWidget(form)
        left.addStretch(1)
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)

        right = QtWidgets.QVBoxLayout()
        error = make_error_banner()
        right.addWidget(error)
        figure = Figure(figsize=(5, 3))
        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(240)
        right.addWidget(canvas, 2)
        right.addStretch(1)

        def calculate() -> None:
            try:
                shock_list = parse_list_floats(shocks.text())
                data = ScenarioInput(base_value=base.value(), shocks=shock_list)
                result = scenario(data)
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            figure.clear()
            ax = figure.add_subplot(111)
            labels = [str(s) for s in shock_list]
            colors = ["#0ea5e9" if val >= 0 else "#f97316" for val in result.outcomes]
            ax.bar(labels, result.outcomes, color=colors)
            ax.axhline(base.value(), color="#94a3b8", linewidth=1)
            ax.text(len(labels) - 0.6, base.value(), "Base", va="bottom", ha="left", fontsize=9, color="#64748b")
            ax.set_xlabel("Shock (%)")
            ax.set_ylabel("Outcome")
            apply_chart_theme(ax)
            format_currency_axis(ax, "y")
            figure.tight_layout()
            canvas.draw()

        left.addWidget(make_primary_button("Calculate", calculate))
        calculate()

        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([320, 800])
        layout.addWidget(splitter)
        return widget

    def _build_sensitivity_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        base = QtWidgets.QDoubleSpinBox()
        base.setRange(0, 1_000_000_000)
        base.setValue(10000)

        change = QtWidgets.QDoubleSpinBox()
        change.setRange(-100, 100)
        change.setValue(10)
        change.setSuffix("%")

        form = make_form(
            [
                labeled_field("Base value", base),
                labeled_field("Change", change),
            ]
        )

        left = QtWidgets.QVBoxLayout()
        left.addWidget(form)
        left.addStretch(1)
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)

        right = QtWidgets.QVBoxLayout()
        error = make_error_banner()
        right.addWidget(error)
        card = ResultCard("New value", "$0")
        card_pct = ResultCard("Percent change", "0%")
        cards = QtWidgets.QHBoxLayout()
        cards.addWidget(card)
        cards.addWidget(card_pct)
        right.addLayout(cards)
        figure = Figure(figsize=(5, 3))
        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(240)
        right.addWidget(canvas, 2)
        right.addStretch(1)

        def calculate() -> None:
            try:
                data = SensitivityInput(base_value=base.value(), change=change.value())
                result = sensitivity(data)
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card.set_value(f"${result.new_value:,.2f}")
            card_pct.set_value(f"{result.percent_change * 100:.2f}%")
            figure.clear()
            ax = figure.add_subplot(111)
            ax.bar(["Base", "New"], [base.value(), result.new_value], color=["#94a3b8", "#0ea5e9"])
            ax.set_ylabel("Value")
            apply_chart_theme(ax)
            format_currency_axis(ax, "y")
            annotate_bars(ax, fmt="${:,.0f}")
            figure.tight_layout()
            canvas.draw()

        left.addWidget(make_primary_button("Calculate", calculate))
        calculate()

        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([320, 800])
        layout.addWidget(splitter)
        return widget

    def _build_monte_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        initial = QtWidgets.QDoubleSpinBox()
        initial.setRange(0, 1_000_000_000)
        initial.setValue(10000)

        mean = QtWidgets.QDoubleSpinBox()
        mean.setRange(-100, 100)
        mean.setValue(7)
        mean.setSuffix("%")

        volatility = QtWidgets.QDoubleSpinBox()
        volatility.setRange(0, 100)
        volatility.setValue(15)
        volatility.setSuffix("%")

        years = QtWidgets.QSpinBox()
        years.setRange(1, 100)
        years.setValue(20)

        sims = QtWidgets.QSpinBox()
        sims.setRange(100, 100000)
        sims.setValue(1000)

        seed = QtWidgets.QSpinBox()
        seed.setRange(0, 1_000_000)
        seed.setValue(42)

        form = make_form(
            [
                labeled_field("Initial value", initial),
                labeled_field("Mean return", mean),
                labeled_field("Volatility", volatility),
                labeled_field("Years", years),
                labeled_field("Simulations", sims),
                labeled_field("Seed", seed),
            ]
        )

        left = QtWidgets.QVBoxLayout()
        left.addWidget(form)
        left.addStretch(1)
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)

        right = QtWidgets.QVBoxLayout()
        error = make_error_banner()
        right.addWidget(error)
        card_mean = ResultCard("Mean", "$0")
        card_median = ResultCard("Median", "$0")
        card_p5 = ResultCard("P5", "$0")
        card_p95 = ResultCard("P95", "$0")
        cards = QtWidgets.QHBoxLayout()
        cards.addWidget(card_mean)
        cards.addWidget(card_median)
        cards.addWidget(card_p5)
        cards.addWidget(card_p95)
        right.addLayout(cards)

        figure = Figure(figsize=(5, 3))
        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(240)
        right.addWidget(canvas, 2)
        right.addStretch(1)

        def calculate() -> None:
            try:
                data = MonteCarloInput(
                    initial_value=initial.value(),
                    mean_return=mean.value(),
                    volatility=volatility.value(),
                    years=years.value(),
                    simulations=sims.value(),
                    seed=seed.value(),
                )
                result = monte_carlo(data)
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card_mean.set_value(f"${result.mean:,.2f}")
            card_median.set_value(f"${result.median:,.2f}")
            card_p5.set_value(f"${result.p5:,.2f}")
            card_p95.set_value(f"${result.p95:,.2f}")
            figure.clear()
            ax = figure.add_subplot(111)
            ax.hist(result.values, bins=35, color="#0ea5e9", alpha=0.85, edgecolor="#ffffff")
            ax.axvspan(result.p5, result.p95, color="#bae6fd", alpha=0.35, label="P5–P95")
            ax.axvline(result.p5, color="#94a3b8", linestyle="--", linewidth=1)
            ax.axvline(result.median, color="#0f172a", linestyle="-", linewidth=1.2, label="Median")
            ax.axvline(result.p95, color="#94a3b8", linestyle="--", linewidth=1)
            ax.axvline(result.mean, color="#38bdf8", linestyle="-.", linewidth=1.2, label="Mean")
            ax.set_xlabel("Final value")
            ax.set_ylabel("Frequency")
            ax.legend(frameon=False, fontsize=9)
            apply_chart_theme(ax)
            format_currency_axis(ax, "x")
            figure.tight_layout()
            canvas.draw()

        left.addWidget(make_primary_button("Calculate", calculate))
        calculate()

        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([320, 800])
        layout.addWidget(splitter)
        return widget

    def _build_stress_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        base = QtWidgets.QDoubleSpinBox()
        base.setRange(0, 1_000_000_000)
        base.setValue(10000)

        drawdown = QtWidgets.QDoubleSpinBox()
        drawdown.setRange(0, 1)
        drawdown.setValue(0.2)
        drawdown.setDecimals(3)

        form = make_form(
            [
                labeled_field("Base value", base),
                labeled_field("Drawdown", drawdown),
            ]
        )

        left = QtWidgets.QVBoxLayout()
        left.addWidget(form)
        left.addStretch(1)
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)

        right = QtWidgets.QVBoxLayout()
        error = make_error_banner()
        right.addWidget(error)
        card = ResultCard("Stressed value", "$0")
        right.addWidget(card)
        figure = Figure(figsize=(5, 3))
        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(240)
        right.addWidget(canvas, 2)
        right.addStretch(1)

        def calculate() -> None:
            try:
                data = StressTestInput(base_value=base.value(), drawdown=drawdown.value())
                result = stress_test(data)
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card.set_value(f"${result.stressed_value:,.2f}")
            figure.clear()
            ax = figure.add_subplot(111)
            ax.bar(["Base", "Stressed"], [base.value(), result.stressed_value], color=["#94a3b8", "#0ea5e9"])
            ax.set_ylabel("Value")
            apply_chart_theme(ax)
            format_currency_axis(ax, "y")
            annotate_bars(ax, fmt="${:,.0f}")
            figure.tight_layout()
            canvas.draw()

        left.addWidget(make_primary_button("Calculate", calculate))
        calculate()

        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([320, 800])
        layout.addWidget(splitter)
        return widget
