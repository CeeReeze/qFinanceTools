from __future__ import annotations

from PySide6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from qfinancetools.core.timeline import build_unified_timeline
from qfinancetools.models.bonds import BondPriceInput
from qfinancetools.models.investments import InvestmentInput
from qfinancetools.models.loans import LoanInput
from qfinancetools.models.stocks import StockProjectionInput
from qfinancetools.models.timeline import TimelineRequest
from qfinancetools.gui.widgets import (
    apply_chart_theme,
    format_currency_axis,
    labeled_field,
    make_error_banner,
    make_form,
    make_primary_button,
    show_error,
)


class TimelinePage(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        self.months = QtWidgets.QSpinBox()
        self.months.setRange(1, 1200)
        self.months.setValue(240)

        self.include_loan = QtWidgets.QCheckBox("Include loan")
        self.include_loan.setChecked(True)
        self.include_invest = QtWidgets.QCheckBox("Include investment")
        self.include_invest.setChecked(True)
        self.include_bonds = QtWidgets.QCheckBox("Include bonds")
        self.include_bonds.setChecked(True)
        self.include_stocks = QtWidgets.QCheckBox("Include stocks/ETF")
        self.include_stocks.setChecked(True)

        left = QtWidgets.QVBoxLayout()
        left.addWidget(make_form([labeled_field("Timeline months", self.months)]))
        left.addWidget(self.include_loan)
        left.addWidget(self.include_invest)
        left.addWidget(self.include_bonds)
        left.addWidget(self.include_stocks)
        left.addStretch(1)
        left.addWidget(make_primary_button("Build timeline", self._calculate))
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)

        right = QtWidgets.QVBoxLayout()
        self.error = make_error_banner()
        right.addWidget(self.error)
        self.figure = Figure(figsize=(6, 3))
        self.canvas = FigureCanvas(self.figure)
        right.addWidget(self.canvas, 2)
        self.summary = QtWidgets.QLabel("")
        self.summary.setWordWrap(True)
        right.addWidget(self.summary)
        right.addStretch(1)
        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 820])
        layout.addWidget(splitter)
        self._calculate()

    def _calculate(self) -> None:
        try:
            request = TimelineRequest(
                months=self.months.value(),
                include_loan=self.include_loan.isChecked(),
                include_invest=self.include_invest.isChecked(),
                include_bonds=self.include_bonds.isChecked(),
                include_stocks=self.include_stocks.isChecked(),
            )
            result = build_unified_timeline(
                request,
                loan_input=LoanInput(principal=350000, annual_rate=5.4, years=25, extra_payment=0),
                invest_input=InvestmentInput(initial=10000, monthly=500, annual_rate=7, years=20),
                bond_input=BondPriceInput(face_value=1000, coupon_rate=5, yield_rate=4.5, years=10, payments_per_year=2),
                stock_input=StockProjectionInput(
                    ticker="SPY",
                    initial=5000,
                    monthly=300,
                    annual_return=8,
                    years=20,
                    expense_ratio=0.03,
                ),
            )
            show_error(self.error, None)
        except Exception as exc:
            show_error(self.error, str(exc))
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        months = [point.month for point in result.net]
        net_values = [point.running_total for point in result.net]
        ax.plot(months, net_values, color="#0ea5e9", linewidth=2, label="Net")
        for series in result.series:
            ax.plot(
                [point.month for point in series.points],
                [point.running_total for point in series.points],
                linewidth=1,
                alpha=0.55,
                label=series.name,
            )
        ax.set_xlabel("Month")
        ax.set_ylabel("Cumulative cash flow")
        ax.legend(frameon=False, fontsize=8)
        apply_chart_theme(ax)
        format_currency_axis(ax, "y")
        self.figure.tight_layout()
        self.canvas.draw()

        warn_count = len(result.warnings)
        net_final = net_values[-1] if net_values else 0.0
        self.summary.setText(f"Final net cumulative cash flow: ${net_final:,.2f}. Warnings: {warn_count}.")
