from __future__ import annotations

from rich.console import Console
from rich.table import Table

from qfinancetools.models.goals import InvestmentGoalResult, LoanPayoffGoalResult


def render_investment_goal(result: InvestmentGoalResult) -> None:
    table = Table(title="Investment Goal")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Target Value", f"{result.target_value:,.2f}")
    table.add_row("Years", str(result.years))
    if result.required_monthly is not None:
        table.add_row("Required Monthly Contribution", f"{result.required_monthly:,.2f}")
    if result.required_annual_rate is not None:
        table.add_row("Required Annual Return", f"{result.required_annual_rate:,.4f}%")
    Console().print(table)


def render_loan_goal(result: LoanPayoffGoalResult) -> None:
    table = Table(title="Loan Payoff Goal")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Base Monthly Payment", f"{result.base_monthly_payment:,.2f}")
    table.add_row("Required Extra Payment", f"{result.required_extra_payment:,.2f}")
    table.add_row("Target Years", str(result.target_years))
    Console().print(table)
