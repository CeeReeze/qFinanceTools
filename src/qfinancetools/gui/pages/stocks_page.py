from __future__ import annotations

from PySide6 import QtCore
from PySide6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from qfinancetools.core.stocks import stock_backtest, stock_history, stock_projection
from qfinancetools.models.stocks import StockBacktestInput, StockHistoryInput, StockProjectionInput
from qfinancetools.gui.widgets import (
    ResultCard,
    apply_chart_theme,
    format_currency_axis,
    labeled_field,
    make_error_banner,
    make_form,
    make_primary_button,
    show_error,
)


class StocksPage(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self._build_projection_tab(), "Projection")
        tabs.addTab(self._build_history_tab(), "History")
        tabs.addTab(self._build_backtest_tab(), "Backtest")
        layout.addWidget(tabs)

    def _build_projection_tab(self) -> QtWidgets.QWidget:
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        ticker = QtWidgets.QLineEdit("SPY")
        initial = QtWidgets.QDoubleSpinBox()
        initial.setRange(0, 1_000_000_000)
        initial.setValue(10000)
        initial.setPrefix("$")
        monthly = QtWidgets.QDoubleSpinBox()
        monthly.setRange(0, 1_000_000)
        monthly.setValue(500)
        monthly.setPrefix("$")
        rate = QtWidgets.QDoubleSpinBox()
        rate.setRange(0, 100)
        rate.setValue(8)
        rate.setSuffix("%")
        years = QtWidgets.QSpinBox()
        years.setRange(1, 100)
        years.setValue(20)
        expense = QtWidgets.QDoubleSpinBox()
        expense.setRange(0, 10)
        expense.setValue(0.03)
        expense.setSuffix("%")
        expense.setDecimals(3)

        form = make_form(
            [
                labeled_field("Ticker", ticker),
                labeled_field("Initial", initial),
                labeled_field("Monthly", monthly),
                labeled_field("Expected return", rate),
                labeled_field("Years", years),
                labeled_field("Expense ratio", expense),
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
        card_return = ResultCard("Effective annual return", "0%")
        card_final = ResultCard("Final value", "$0")
        card_contrib = ResultCard("Contributions", "$0")
        card_growth = ResultCard("Growth", "$0")
        cards = QtWidgets.QHBoxLayout()
        cards.addWidget(card_return)
        cards.addWidget(card_final)
        cards.addWidget(card_contrib)
        cards.addWidget(card_growth)
        right.addLayout(cards)
        warning = QtWidgets.QLabel("")
        warning.setWordWrap(True)
        right.addWidget(warning)
        right.addStretch(1)
        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)

        def calculate() -> None:
            try:
                result = stock_projection(
                    StockProjectionInput(
                        ticker=ticker.text().strip() or "ETF",
                        initial=initial.value(),
                        monthly=monthly.value(),
                        annual_return=rate.value(),
                        years=years.value(),
                        expense_ratio=expense.value(),
                    )
                )
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card_return.set_value(f"{result.effective_annual_return:,.2f}%")
            card_final.set_value(f"${result.final_value:,.2f}")
            card_contrib.set_value(f"${result.total_contributions:,.2f}")
            card_growth.set_value(f"${result.total_growth:,.2f}")
            if result.warnings:
                warning.setText("Warnings: " + " | ".join(item.message for item in result.warnings))
            else:
                warning.setText("")

        left.addWidget(make_primary_button("Calculate", calculate))
        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([320, 800])
        layout.addWidget(splitter)
        return tab

    def _build_history_tab(self) -> QtWidgets.QWidget:
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        tickers = QtWidgets.QLineEdit("SPY,QQQ")
        weights = QtWidgets.QLineEdit("")
        period_years = QtWidgets.QSpinBox()
        period_years.setRange(1, 50)
        period_years.setValue(5)
        use_dates = QtWidgets.QCheckBox("Use explicit date range")
        use_dates.setChecked(False)
        start_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate().addYears(-5))
        start_date.setCalendarPopup(True)
        start_date.setDisplayFormat("yyyy-MM-dd")
        end_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        end_date.setCalendarPopup(True)
        end_date.setDisplayFormat("yyyy-MM-dd")
        start_date.setEnabled(False)
        end_date.setEnabled(False)
        use_dates.toggled.connect(start_date.setEnabled)
        use_dates.toggled.connect(end_date.setEnabled)

        left = QtWidgets.QVBoxLayout()
        left.addWidget(
            make_form(
                [
                    labeled_field("Tickers (comma separated)", tickers),
                    labeled_field("Weights (comma separated)", weights),
                    labeled_field("Period years", period_years),
                    labeled_field("Date mode", use_dates),
                    labeled_field("Start date", start_date),
                    labeled_field("End date", end_date),
                ]
            )
        )
        left.addStretch(1)

        right = QtWidgets.QVBoxLayout()
        error = make_error_banner()
        right.addWidget(error)
        freshness = QtWidgets.QLabel("")
        right.addWidget(freshness)
        figure = Figure(figsize=(5, 3))
        canvas = FigureCanvas(figure)
        right.addWidget(canvas, 2)
        right.addStretch(1)

        def calculate() -> None:
            try:
                ticker_list = [item.strip().upper() for item in tickers.text().split(",") if item.strip()]
                weight_values = [float(item.strip()) for item in weights.text().split(",") if item.strip()]
                result = stock_history(
                    StockHistoryInput(
                        tickers=ticker_list,
                        start_date=start_date.date().toString("yyyy-MM-dd") if use_dates.isChecked() else None,
                        end_date=end_date.date().toString("yyyy-MM-dd") if use_dates.isChecked() else None,
                        period_years=period_years.value(),
                        weights=weight_values or None,
                    )
                )
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return

            figure.clear()
            ax = figure.add_subplot(111)
            for series in result.series:
                x = list(range(len(series.points)))
                y = [point.normalized for point in series.points]
                width = 2 if series.name == "PORTFOLIO" else 1
                ax.plot(x, y, linewidth=width, label=series.name)
            ax.set_xlabel("Time")
            ax.set_ylabel("Normalized index (start=100)")
            ax.legend(frameon=False, fontsize=8)
            apply_chart_theme(ax)
            figure.tight_layout()
            canvas.draw()
            stale = any(series.stale for series in result.series)
            freshness.setText(
                f"Source: {result.source} | Window: {result.start_date} -> {result.end_date} | stale: {'yes' if stale else 'no'}"
            )

        left.addWidget(make_primary_button("Load history", calculate))
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)
        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)
        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([320, 800])
        layout.addWidget(splitter)
        return tab

    def _build_backtest_tab(self) -> QtWidgets.QWidget:
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        tickers = QtWidgets.QLineEdit("SPY")
        weights = QtWidgets.QLineEdit("")
        period_years = QtWidgets.QSpinBox()
        period_years.setRange(1, 50)
        period_years.setValue(5)
        use_dates = QtWidgets.QCheckBox("Use explicit date range")
        use_dates.setChecked(False)
        start_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate().addYears(-5))
        start_date.setCalendarPopup(True)
        start_date.setDisplayFormat("yyyy-MM-dd")
        end_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        end_date.setCalendarPopup(True)
        end_date.setDisplayFormat("yyyy-MM-dd")
        start_date.setEnabled(False)
        end_date.setEnabled(False)
        use_dates.toggled.connect(start_date.setEnabled)
        use_dates.toggled.connect(end_date.setEnabled)
        lump_sum = QtWidgets.QDoubleSpinBox()
        lump_sum.setRange(0, 1_000_000_000)
        lump_sum.setValue(10000)
        lump_sum.setPrefix("$")
        periodic = QtWidgets.QDoubleSpinBox()
        periodic.setRange(0, 1_000_000)
        periodic.setValue(500)
        periodic.setPrefix("$")
        periodic_months = QtWidgets.QSpinBox()
        periodic_months.setRange(1, 24)
        periodic_months.setValue(1)

        left = QtWidgets.QVBoxLayout()
        left.addWidget(
            make_form(
                [
                    labeled_field("Tickers (comma separated)", tickers),
                    labeled_field("Weights (comma separated)", weights),
                    labeled_field("Period years", period_years),
                    labeled_field("Date mode", use_dates),
                    labeled_field("Start date", start_date),
                    labeled_field("End date", end_date),
                    labeled_field("Lump sum", lump_sum),
                    labeled_field("Periodic amount", periodic),
                    labeled_field("Periodicity (months)", periodic_months),
                ]
            )
        )
        left.addStretch(1)

        right = QtWidgets.QVBoxLayout()
        error = make_error_banner()
        right.addWidget(error)
        card_invested = ResultCard("Final invested", "$0")
        card_value = ResultCard("Final value", "$0")
        card_revenue = ResultCard("Revenue", "$0")
        card_return = ResultCard("Return %", "0%")
        cards = QtWidgets.QHBoxLayout()
        cards.addWidget(card_invested)
        cards.addWidget(card_value)
        cards.addWidget(card_revenue)
        cards.addWidget(card_return)
        right.addLayout(cards)
        figure = Figure(figsize=(5, 3))
        canvas = FigureCanvas(figure)
        right.addWidget(canvas, 2)
        right.addStretch(1)

        def calculate() -> None:
            try:
                ticker_list = [item.strip().upper() for item in tickers.text().split(",") if item.strip()]
                weight_values = [float(item.strip()) for item in weights.text().split(",") if item.strip()]
                result = stock_backtest(
                    StockBacktestInput(
                        tickers=ticker_list,
                        start_date=start_date.date().toString("yyyy-MM-dd") if use_dates.isChecked() else None,
                        end_date=end_date.date().toString("yyyy-MM-dd") if use_dates.isChecked() else None,
                        period_years=period_years.value(),
                        lump_sum=lump_sum.value(),
                        periodic_amount=periodic.value(),
                        periodic_months=periodic_months.value(),
                        weights=weight_values or None,
                    )
                )
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return

            card_invested.set_value(f"${result.final_invested:,.2f}")
            card_value.set_value(f"${result.final_value:,.2f}")
            card_revenue.set_value(f"${result.final_revenue:,.2f}")
            card_return.set_value(f"{result.final_return_percent:,.2f}%")

            figure.clear()
            ax = figure.add_subplot(111)
            x = list(range(len(result.timeline)))
            invested = [point.invested for point in result.timeline]
            value = [point.value for point in result.timeline]
            ax.plot(x, invested, label="Invested", color="#94a3b8", linewidth=2)
            ax.plot(x, value, label="Portfolio value", color="#0ea5e9", linewidth=2)
            ax.set_xlabel("Time")
            ax.set_ylabel("Amount")
            ax.legend(frameon=False, fontsize=8)
            apply_chart_theme(ax)
            format_currency_axis(ax, "y")
            figure.tight_layout()
            canvas.draw()

        left.addWidget(make_primary_button("Run backtest", calculate))
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)
        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)
        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([320, 800])
        layout.addWidget(splitter)
        return tab
