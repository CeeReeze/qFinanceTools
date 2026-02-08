from __future__ import annotations

from PySide6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from qfinancetools.core.corporate import wacc, capm, npv, irr, dcf, comps
from qfinancetools.models.corporate import (
    WaccInput,
    CapmInput,
    NpvInput,
    IrrInput,
    DcfInput,
    CompsInput,
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
    format_percent_axis,
)


class CorporatePage(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self._build_wacc_tab(), "WACC")
        tabs.addTab(self._build_capm_tab(), "CAPM")
        tabs.addTab(self._build_npv_tab(), "NPV")
        tabs.addTab(self._build_irr_tab(), "IRR")
        tabs.addTab(self._build_dcf_tab(), "DCF")
        tabs.addTab(self._build_comps_tab(), "Comps")

        layout.addWidget(tabs)

    def _build_wacc_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        cost_equity = QtWidgets.QDoubleSpinBox()
        cost_equity.setRange(0, 100)
        cost_equity.setValue(9)
        cost_equity.setSuffix("%")
        cost_equity.setDecimals(3)

        cost_debt = QtWidgets.QDoubleSpinBox()
        cost_debt.setRange(0, 100)
        cost_debt.setValue(5.5)
        cost_debt.setSuffix("%")
        cost_debt.setDecimals(3)

        tax_rate = QtWidgets.QDoubleSpinBox()
        tax_rate.setRange(0, 1)
        tax_rate.setValue(0.26)
        tax_rate.setDecimals(3)

        equity_value = QtWidgets.QDoubleSpinBox()
        equity_value.setRange(0, 1_000_000_000)
        equity_value.setValue(12_000_000)
        equity_value.setPrefix("$")

        debt_value = QtWidgets.QDoubleSpinBox()
        debt_value.setRange(0, 1_000_000_000)
        debt_value.setValue(4_500_000)
        debt_value.setPrefix("$")

        form = make_form(
            [
                labeled_field("Cost of equity", cost_equity),
                labeled_field("Cost of debt", cost_debt),
                labeled_field("Tax rate", tax_rate),
                labeled_field("Equity value", equity_value),
                labeled_field("Debt value", debt_value),
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
        card = ResultCard("WACC", "0%")
        right.addWidget(card)
        figure = Figure(figsize=(5, 2.2))
        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(200)
        right.addWidget(canvas)
        right.addStretch(1)

        def calculate() -> None:
            try:
                data = WaccInput(
                    cost_of_equity=cost_equity.value(),
                    cost_of_debt=cost_debt.value(),
                    tax_rate=tax_rate.value(),
                    equity_value=equity_value.value(),
                    debt_value=debt_value.value(),
                )
                result = wacc(data)
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card.set_value(f"{result.wacc:.3f}%")
            figure.clear()
            ax = figure.add_subplot(111)
            max_rate = 20
            ax.barh(["WACC"], [result.wacc], color="#0ea5e9")
            ax.set_xlim(0, max_rate)
            ax.set_xlabel("Percent")
            apply_chart_theme(ax)
            format_percent_axis(ax, "x")
            ax.text(result.wacc, 0, f"{result.wacc:.2f}%", va="center", ha="left", fontsize=9)
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

    def _build_capm_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        risk_free = QtWidgets.QDoubleSpinBox()
        risk_free.setRange(0, 100)
        risk_free.setValue(4)
        risk_free.setSuffix("%")
        risk_free.setDecimals(3)

        beta = QtWidgets.QDoubleSpinBox()
        beta.setRange(-5, 5)
        beta.setValue(1.1)
        beta.setDecimals(3)

        market_return = QtWidgets.QDoubleSpinBox()
        market_return.setRange(0, 100)
        market_return.setValue(9)
        market_return.setSuffix("%")
        market_return.setDecimals(3)

        form = make_form(
            [
                labeled_field("Risk-free rate", risk_free),
                labeled_field("Beta", beta),
                labeled_field("Market return", market_return),
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
        card = ResultCard("Cost of equity", "0%")
        right.addWidget(card)
        figure = Figure(figsize=(5, 2.2))
        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(200)
        right.addWidget(canvas)
        right.addStretch(1)

        def calculate() -> None:
            try:
                data = CapmInput(
                    risk_free_rate=risk_free.value(),
                    beta=beta.value(),
                    market_return=market_return.value(),
                )
                result = capm(data)
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card.set_value(f"{result.cost_of_equity:.3f}%")
            figure.clear()
            ax = figure.add_subplot(111)
            max_rate = 20
            ax.barh(["Cost of equity"], [result.cost_of_equity], color="#0ea5e9")
            ax.set_xlim(0, max_rate)
            ax.set_xlabel("Percent")
            apply_chart_theme(ax)
            format_percent_axis(ax, "x")
            ax.text(result.cost_of_equity, 0, f"{result.cost_of_equity:.2f}%", va="center", ha="left", fontsize=9)
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

    def _build_npv_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        rate = QtWidgets.QDoubleSpinBox()
        rate.setRange(0, 100)
        rate.setValue(9)
        rate.setSuffix("%")
        rate.setDecimals(3)

        cash_flows = QtWidgets.QLineEdit("-100000, 30000, 40000, 50000")

        form = make_form(
            [
                labeled_field("Discount rate", rate),
                labeled_field("Cash flows", cash_flows),
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
        card = ResultCard("Net present value", "$0")
        right.addWidget(card)
        figure = Figure(figsize=(5, 3))
        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(240)
        right.addWidget(canvas, 2)
        right.addStretch(1)

        def calculate() -> None:
            try:
                flows = parse_list_floats(cash_flows.text())
                data = NpvInput(discount_rate=rate.value(), cash_flows=flows)
                result = npv(data)
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card.set_value(f"${result.npv:,.2f}")
            figure.clear()
            ax = figure.add_subplot(111)
            colors = ["#0ea5e9" if val >= 0 else "#f97316" for val in flows]
            ax.bar([str(i) for i in range(len(flows))], flows, color=colors)
            ax.axhline(0, color="#94a3b8", linewidth=1)
            ax.set_xlabel("Period")
            ax.set_ylabel("Cash flow")
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

    def _build_irr_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        cash_flows = QtWidgets.QLineEdit("-100000, 30000, 40000, 50000")
        guess = QtWidgets.QDoubleSpinBox()
        guess.setRange(-0.99, 10)
        guess.setValue(0.1)
        guess.setDecimals(4)

        form = make_form(
            [
                labeled_field("Cash flows", cash_flows),
                labeled_field("Guess (decimal)", guess),
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
        card = ResultCard("Internal rate of return", "0%")
        right.addWidget(card)
        figure = Figure(figsize=(5, 3))
        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(240)
        right.addWidget(canvas, 2)
        right.addStretch(1)

        def calculate() -> None:
            try:
                flows = parse_list_floats(cash_flows.text())
                data = IrrInput(cash_flows=flows, guess=guess.value())
                result = irr(data)
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card.set_value(f"{result.irr:.3f}%")
            figure.clear()
            ax = figure.add_subplot(111)
            colors = ["#f97316" if val < 0 else "#0ea5e9" for val in flows]
            ax.bar([str(i) for i in range(len(flows))], flows, color=colors)
            ax.axhline(0, color="#94a3b8", linewidth=1)
            ax.set_xlabel("Period")
            ax.set_ylabel("Cash flow")
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

    def _build_dcf_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        rate = QtWidgets.QDoubleSpinBox()
        rate.setRange(0, 100)
        rate.setValue(9)
        rate.setSuffix("%")
        rate.setDecimals(3)

        cash_flows = QtWidgets.QLineEdit("100000, 120000, 140000")
        terminal_growth = QtWidgets.QDoubleSpinBox()
        terminal_growth.setRange(-0.99, 1)
        terminal_growth.setValue(0.02)
        terminal_growth.setDecimals(4)

        terminal_multiple = QtWidgets.QLineEdit("")

        form = make_form(
            [
                labeled_field("Discount rate", rate),
                labeled_field("Cash flows", cash_flows),
                labeled_field("Terminal growth", terminal_growth),
                labeled_field("Terminal multiple (optional)", terminal_multiple),
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
        card_pv = ResultCard("Present value", "$0")
        card_terminal = ResultCard("Terminal value", "$0")
        card_total = ResultCard("Total value", "$0")
        cards = QtWidgets.QHBoxLayout()
        cards.addWidget(card_pv)
        cards.addWidget(card_terminal)
        cards.addWidget(card_total)
        right.addLayout(cards)
        figure = Figure(figsize=(5, 3))
        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(240)
        right.addWidget(canvas, 2)
        right.addStretch(1)

        def calculate() -> None:
            try:
                flows = parse_list_floats(cash_flows.text())
                multiple_text = terminal_multiple.text().strip()
                multiple = float(multiple_text) if multiple_text else None
                data = DcfInput(
                    discount_rate=rate.value(),
                    cash_flows=flows,
                    terminal_growth=terminal_growth.value(),
                    terminal_multiple=multiple,
                )
                result = dcf(data)
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card_pv.set_value(f"${result.present_value:,.2f}")
            card_terminal.set_value(f"${result.terminal_value:,.2f}")
            card_total.set_value(f"${result.total_value:,.2f}")
            figure.clear()
            ax = figure.add_subplot(111)
            ax.bar(["PV", "Terminal", "Total"], [result.present_value, result.terminal_value, result.total_value],
                   color=["#94a3b8", "#38bdf8", "#0ea5e9"])
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

    def _build_comps_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        metric = QtWidgets.QDoubleSpinBox()
        metric.setRange(0, 1_000_000_000)
        metric.setValue(100)

        multiples = QtWidgets.QLineEdit("6, 7.5, 8, 10")

        form = make_form(
            [
                labeled_field("Metric value", metric),
                labeled_field("Multiples", multiples),
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
        card_low = ResultCard("Low", "$0")
        card_med = ResultCard("Median", "$0")
        card_high = ResultCard("High", "$0")
        cards = QtWidgets.QHBoxLayout()
        cards.addWidget(card_low)
        cards.addWidget(card_med)
        cards.addWidget(card_high)
        right.addLayout(cards)

        figure = Figure(figsize=(5, 3))
        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(240)
        right.addWidget(canvas, 2)
        right.addStretch(1)

        def calculate() -> None:
            try:
                mults = parse_list_floats(multiples.text())
                data = CompsInput(metric=metric.value(), multiples=mults)
                result = comps(data)
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card_low.set_value(f"${result.low:,.2f}")
            card_med.set_value(f"${result.median:,.2f}")
            card_high.set_value(f"${result.high:,.2f}")
            figure.clear()
            ax = figure.add_subplot(111)
            ax.barh(["Range"], [result.high - result.low], left=[result.low], color="#bae6fd")
            ax.plot(result.median, 0, "o", color="#0f172a")
            ax.text(result.low, 0, f"${result.low:,.0f}", va="center", ha="right", fontsize=9)
            ax.text(result.high, 0, f"${result.high:,.0f}", va="center", ha="left", fontsize=9)
            ax.set_xlabel("Value range")
            ax.set_yticks([])
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
