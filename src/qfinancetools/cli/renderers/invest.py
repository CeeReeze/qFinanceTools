from __future__ import annotations

from rich.console import Console
from rich.table import Table

from qfinancetools.models.investments import InvestmentResult


def render_investment_summary(result: InvestmentResult) -> None:
    table = Table(title="Investment Summary")
    table.add_column("Metric")
    table.add_column("Value", justify="right")

    table.add_row("Final Value", f"{result.final_value:,.2f}")
    table.add_row("Total Contributions", f"{result.total_contributions:,.2f}")
    table.add_row("Total Growth", f"{result.total_growth:,.2f}")
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
