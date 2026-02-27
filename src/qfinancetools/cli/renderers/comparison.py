from __future__ import annotations

from rich.console import Console
from rich.table import Table

from qfinancetools.models.comparison import ComparisonResult


def render_comparison(result: ComparisonResult) -> None:
    table = Table(title=f"Comparison ({result.calculator})")
    table.add_column("Metric")
    table.add_column(result.base_label, justify="right")
    table.add_column(result.alt_label, justify="right")
    table.add_column("Delta", justify="right")
    table.add_column("Delta %", justify="right")

    for delta in result.deltas:
        pct = f"{delta.percent_delta:,.2f}%" if delta.percent_delta is not None else delta.percent_delta_reason or "n/a"
        table.add_row(
            delta.metric,
            f"{delta.base_value:,.2f}",
            f"{delta.alt_value:,.2f}",
            f"{delta.absolute_delta:,.2f}",
            pct,
        )
    Console().print(table)
