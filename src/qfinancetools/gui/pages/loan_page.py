from __future__ import annotations

from PySide6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from qfinancetools.core.loans import amortization_schedule, loan_summary
from qfinancetools.models.loans import LoanInput
from qfinancetools.gui.widgets import (
    labeled_field,
    make_error_banner,
    make_form,
    make_primary_button,
    show_error,
    ResultCard,
    apply_chart_theme,
    format_currency_axis,
)


class LoanPage(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        self.amount = QtWidgets.QDoubleSpinBox()
        self.amount.setRange(0, 1_000_000_000)
        self.amount.setValue(350000)
        self.amount.setPrefix("$")
        self.amount.setDecimals(2)

        self.rate = QtWidgets.QDoubleSpinBox()
        self.rate.setRange(0, 100)
        self.rate.setValue(5.4)
        self.rate.setSuffix("%")
        self.rate.setDecimals(3)

        self.years = QtWidgets.QSpinBox()
        self.years.setRange(1, 100)
        self.years.setValue(25)

        self.extra = QtWidgets.QDoubleSpinBox()
        self.extra.setRange(0, 1_000_000)
        self.extra.setValue(0)
        self.extra.setPrefix("$")
        self.extra.setDecimals(2)

        self.show_table = QtWidgets.QCheckBox("Show amortization table")
        self.show_table.setChecked(True)
        self.show_table.toggled.connect(self._calculate)

        form = make_form(
            [
                labeled_field("Loan principal", self.amount),
                labeled_field("Annual rate", self.rate),
                labeled_field("Term (years)", self.years),
                labeled_field("Extra monthly", self.extra),
            ]
        )

        left = QtWidgets.QVBoxLayout()
        left.addWidget(form)
        left.addWidget(self.show_table)
        left.addStretch(1)
        left.addWidget(make_primary_button("Calculate", self._calculate))
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)

        right = QtWidgets.QVBoxLayout()
        self.error_banner = make_error_banner()
        right.addWidget(self.error_banner)

        self.card_payment = ResultCard("Monthly payment", "$0")
        self.card_interest = ResultCard("Total interest", "$0")
        self.card_total = ResultCard("Total paid", "$0")
        self.card_years = ResultCard("Actual years", "0")
        cards = QtWidgets.QHBoxLayout()
        cards.addWidget(self.card_payment)
        cards.addWidget(self.card_interest)
        cards.addWidget(self.card_total)
        cards.addWidget(self.card_years)
        right.addLayout(cards)

        self.table = QtWidgets.QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Month", "Payment", "Principal", "Interest", "Balance"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setMinimumHeight(160)

        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(240)

        right.addWidget(self.canvas, 2)
        right.addWidget(self.table, 1)
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
            data = LoanInput(
                principal=self.amount.value(),
                annual_rate=self.rate.value(),
                years=self.years.value(),
                extra_payment=self.extra.value(),
            )
            summary = loan_summary(data)
            show_error(self.error_banner, None)
        except Exception as exc:
            show_error(self.error_banner, str(exc))
            return

        self.card_payment.set_value(f"${summary.monthly_payment:,.2f}")
        self.card_interest.set_value(f"${summary.total_interest:,.2f}")
        self.card_total.set_value(f"${summary.total_paid:,.2f}")
        self.card_years.set_value(f"{summary.years:.2f}")

        rows = amortization_schedule(data)
        self._render_table(rows if self.show_table.isChecked() else [])
        self._render_chart(rows)

    def _render_table(self, rows) -> None:
        self.table.setVisible(bool(rows))
        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            values = [
                str(row.month),
                f"${row.payment:,.2f}",
                f"${row.principal:,.2f}",
                f"${row.interest:,.2f}",
                f"${row.balance:,.2f}",
            ]
            for col_idx, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(value)
                self.table.setItem(row_idx, col_idx, item)

    def _render_chart(self, rows) -> None:
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if rows:
            months = [row.month for row in rows]
            balances = [row.balance for row in rows]
            ax.plot(months, balances, color="#0ea5e9", linewidth=2)
            ax.fill_between(months, balances, color="#bae6fd", alpha=0.6)
            ax.set_xlabel("Month")
            ax.set_ylabel("Balance")
            apply_chart_theme(ax)
            format_currency_axis(ax, "y")
            ax.annotate(
                f"${balances[-1]:,.2f}",
                xy=(months[-1], balances[-1]),
                xytext=(8, 0),
                textcoords="offset points",
                va="center",
                fontsize=9,
                color="#0f172a",
            )
        else:
            ax.text(0.5, 0.5, "Enable schedule to view chart", ha="center", va="center")
            ax.set_axis_off()
        self.figure.tight_layout()
        self.canvas.draw()
