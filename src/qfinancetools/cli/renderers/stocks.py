from __future__ import annotations

from rich.console import Console
from rich.table import Table

from qfinancetools.models.stocks import (
    StockBacktestResult,
    StockHistoryResult,
    StockProjectionResult,
)


def render_stock_projection(result: StockProjectionResult) -> None:
    table = Table(title=f"Stocks/ETF Projection ({result.ticker})")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Effective Annual Return", f"{result.effective_annual_return:,.2f}%")
    table.add_row("Final Value", f"{result.final_value:,.2f}")
    table.add_row("Total Contributions", f"{result.total_contributions:,.2f}")
    table.add_row("Total Growth", f"{result.total_growth:,.2f}")
    Console().print(table)
    if result.warnings:
        warn = Table(title="Warnings")
        warn.add_column("Code")
        warn.add_column("Message")
        for item in result.warnings:
            warn.add_row(item.code, item.message)
        Console().print(warn)


def render_stock_history(result: StockHistoryResult) -> None:
    table = Table(title=f"Stocks/ETF History ({result.start_date} -> {result.end_date})")
    table.add_column("Series")
    table.add_column("Start (Norm)", justify="right")
    table.add_column("End (Norm)", justify="right")
    table.add_column("Change", justify="right")
    table.add_column("Last Updated", justify="right")
    table.add_column("Stale", justify="right")
    for series in result.series:
        start_norm = series.points[0].normalized if series.points else 0.0
        end_norm = series.points[-1].normalized if series.points else 0.0
        change = end_norm - start_norm
        table.add_row(
            series.name,
            f"{start_norm:,.2f}",
            f"{end_norm:,.2f}",
            f"{change:,.2f}",
            series.last_updated,
            "yes" if series.stale else "no",
        )
    Console().print(table)


def render_stock_backtest(result: StockBacktestResult) -> None:
    table = Table(title=f"Stocks/ETF Backtest ({result.start_date} -> {result.end_date})")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Final Invested", f"{result.final_invested:,.2f}")
    table.add_row("Final Value", f"{result.final_value:,.2f}")
    table.add_row("Final Revenue", f"{result.final_revenue:,.2f}")
    table.add_row("Final Return %", f"{result.final_return_percent:,.2f}%")
    table.add_row("Last Updated", result.last_updated)
    table.add_row("Stale", "yes" if result.stale else "no")
    Console().print(table)

    if result.warnings:
        warn = Table(title="Warnings")
        warn.add_column("Code")
        warn.add_column("Message")
        for item in result.warnings:
            warn.add_row(item.code, item.message)
        Console().print(warn)
