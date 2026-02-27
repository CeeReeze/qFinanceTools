from __future__ import annotations

from rich.console import Console
from rich.table import Table

from qfinancetools.models.loans import LoanResult, AmortizationRow


def render_loan_summary(result: LoanResult) -> None:
    table = Table(title="Loan Summary")
    table.add_column("Metric")
    table.add_column("Value", justify="right")

    table.add_row("Monthly Payment", f"{result.monthly_payment:,.2f}")
    table.add_row("Total Interest", f"{result.total_interest:,.2f}")
    table.add_row("Total Paid", f"{result.total_paid:,.2f}")
    table.add_row("Years", f"{result.years:.2f}")

    Console().print(table)
    if result.warnings:
        warnings = Table(title="Warnings")
        warnings.add_column("Code")
        warnings.add_column("Message")
        for item in result.warnings:
            warnings.add_row(item.code, item.message)
        Console().print(warnings)
    if result.explanation:
        explain = Table(title="Explanation")
        explain.add_column("Step")
        explain.add_column("Formula")
        explain.add_column("Value", justify="right")
        for step in result.explanation.steps:
            value = f"{step.value:,.6f}" if isinstance(step.value, float) else str(step.value)
            explain.add_row(step.name, step.formula, value)
        Console().print(explain)


def render_amortization(rows: list[AmortizationRow]) -> None:
    table = Table(title="Amortization Schedule")
    table.add_column("Month", justify="right")
    table.add_column("Payment", justify="right")
    table.add_column("Principal", justify="right")
    table.add_column("Interest", justify="right")
    table.add_column("Balance", justify="right")

    for row in rows:
        table.add_row(
            str(row.month),
            f"{row.payment:,.2f}",
            f"{row.principal:,.2f}",
            f"{row.interest:,.2f}",
            f"{row.balance:,.2f}",
        )

    Console().print(table)
