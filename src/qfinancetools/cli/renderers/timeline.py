from __future__ import annotations

from rich.console import Console
from rich.table import Table

from qfinancetools.models.timeline import TimelineResult


def render_timeline(result: TimelineResult) -> None:
    summary = Table(title="Unified Timeline Summary")
    summary.add_column("Series")
    summary.add_column("Final Running Total", justify="right")
    for series in result.series:
        value = series.points[-1].running_total if series.points else 0.0
        summary.add_row(series.name, f"{value:,.2f}")
    net_final = result.net[-1].running_total if result.net else 0.0
    summary.add_row("Net", f"{net_final:,.2f}")
    Console().print(summary)

    if result.warnings:
        warn = Table(title="Warnings")
        warn.add_column("Code")
        warn.add_column("Message")
        for item in result.warnings:
            warn.add_row(item.code, item.message)
        Console().print(warn)
