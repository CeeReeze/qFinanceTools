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
