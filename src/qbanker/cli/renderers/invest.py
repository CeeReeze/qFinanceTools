from __future__ import annotations

from rich.console import Console
from rich.table import Table

from qbanker.models.investments import InvestmentResult


def render_investment_summary(result: InvestmentResult) -> None:
    table = Table(title="Investment Summary")
    table.add_column("Metric")
    table.add_column("Value", justify="right")

    table.add_row("Final Value", f"{result.final_value:,.2f}")
    table.add_row("Total Contributions", f"{result.total_contributions:,.2f}")
    table.add_row("Total Growth", f"{result.total_growth:,.2f}")
    table.add_row("Years", f"{result.years:.2f}")

    Console().print(table)
