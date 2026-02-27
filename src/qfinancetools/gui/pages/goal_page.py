from __future__ import annotations

from PySide6 import QtWidgets

from qfinancetools.core.goals import solve_investment_goal, solve_loan_payoff_goal
from qfinancetools.models.goals import InvestmentGoalInput, LoanPayoffGoalInput
from qfinancetools.gui.widgets import (
    ResultCard,
    labeled_field,
    make_error_banner,
    make_form,
    make_primary_button,
    show_error,
)


class GoalPage(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self._invest_tab(), "Investment Goal")
        tabs.addTab(self._loan_tab(), "Loan Payoff Goal")
        layout.addWidget(tabs)

    def _invest_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        target = QtWidgets.QDoubleSpinBox()
        target.setRange(1, 1_000_000_000)
        target.setValue(1_000_000)
        target.setPrefix("$")
        initial = QtWidgets.QDoubleSpinBox()
        initial.setRange(0, 1_000_000_000)
        initial.setValue(50_000)
        initial.setPrefix("$")
        years = QtWidgets.QSpinBox()
        years.setRange(1, 100)
        years.setValue(25)
        mode = QtWidgets.QComboBox()
        mode.addItems(["Solve monthly", "Solve annual return"])
        monthly = QtWidgets.QDoubleSpinBox()
        monthly.setRange(0, 1_000_000)
        monthly.setValue(1000)
        monthly.setPrefix("$")
        rate = QtWidgets.QDoubleSpinBox()
        rate.setRange(0, 100)
        rate.setValue(7)
        rate.setSuffix("%")

        left = QtWidgets.QVBoxLayout()
        left.addWidget(
            make_form(
                [
                    labeled_field("Target value", target),
                    labeled_field("Initial value", initial),
                    labeled_field("Years", years),
                    labeled_field("Mode", mode),
                    labeled_field("Known monthly", monthly),
                    labeled_field("Known annual rate", rate),
                ]
            )
        )
        right = QtWidgets.QVBoxLayout()
        error = make_error_banner()
        right.addWidget(error)
        card_monthly = ResultCard("Required monthly", "$0")
        card_rate = ResultCard("Required annual rate", "0%")
        cards = QtWidgets.QHBoxLayout()
        cards.addWidget(card_monthly)
        cards.addWidget(card_rate)
        right.addLayout(cards)
        notes = QtWidgets.QLabel("")
        notes.setWordWrap(True)
        right.addWidget(notes)
        right.addStretch(1)

        def calculate() -> None:
            try:
                if mode.currentText() == "Solve monthly":
                    payload = InvestmentGoalInput(
                        target_value=target.value(),
                        initial=initial.value(),
                        years=years.value(),
                        annual_rate=rate.value(),
                    )
                else:
                    payload = InvestmentGoalInput(
                        target_value=target.value(),
                        initial=initial.value(),
                        years=years.value(),
                        monthly=monthly.value(),
                    )
                result = solve_investment_goal(payload)
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card_monthly.set_value(f"${(result.required_monthly or 0):,.2f}")
            card_rate.set_value(f"{(result.required_annual_rate or 0):,.2f}%")
            notes.setText(result.explanation.summary if result.explanation else "")

        left.addWidget(make_primary_button("Solve", calculate))
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)
        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)
        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([320, 800])
        layout.addWidget(splitter)
        calculate()
        return widget

    def _loan_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        principal = QtWidgets.QDoubleSpinBox()
        principal.setRange(1, 1_000_000_000)
        principal.setValue(350_000)
        principal.setPrefix("$")
        rate = QtWidgets.QDoubleSpinBox()
        rate.setRange(0, 100)
        rate.setValue(5.4)
        rate.setSuffix("%")
        current_years = QtWidgets.QSpinBox()
        current_years.setRange(1, 100)
        current_years.setValue(25)
        target_years = QtWidgets.QSpinBox()
        target_years.setRange(1, 100)
        target_years.setValue(20)

        left = QtWidgets.QVBoxLayout()
        left.addWidget(
            make_form(
                [
                    labeled_field("Principal", principal),
                    labeled_field("Rate", rate),
                    labeled_field("Current years", current_years),
                    labeled_field("Target years", target_years),
                ]
            )
        )
        right = QtWidgets.QVBoxLayout()
        error = make_error_banner()
        right.addWidget(error)
        card_payment = ResultCard("Base monthly payment", "$0")
        card_extra = ResultCard("Required extra payment", "$0")
        cards = QtWidgets.QHBoxLayout()
        cards.addWidget(card_payment)
        cards.addWidget(card_extra)
        right.addLayout(cards)
        right.addStretch(1)

        def calculate() -> None:
            try:
                result = solve_loan_payoff_goal(
                    LoanPayoffGoalInput(
                        principal=principal.value(),
                        annual_rate=rate.value(),
                        current_years=current_years.value(),
                        target_years=target_years.value(),
                    )
                )
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card_payment.set_value(f"${result.base_monthly_payment:,.2f}")
            card_extra.set_value(f"${result.required_extra_payment:,.2f}")

        left.addWidget(make_primary_button("Solve", calculate))
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)
        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)
        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([320, 800])
        layout.addWidget(splitter)
        calculate()
        return widget
