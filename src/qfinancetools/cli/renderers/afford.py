from __future__ import annotations

from rich.console import Console
from rich.table import Table

from qfinancetools.models.afford import AffordResult


def render_affordability(result: AffordResult) -> None:
    table = Table(title="Affordability")
    table.add_column("Metric")
    table.add_column("Value", justify="right")

    table.add_row("Allowed Housing", f"{result.allowed_housing:,.2f}")
    table.add_row("Current DTI", f"{result.current_dti:.3f}")
    table.add_row("Stressed DTI", f"{result.stressed_dti:.3f}")
    table.add_row("Affordable", "Yes" if result.affordable else "No")

    Console().print(table)
