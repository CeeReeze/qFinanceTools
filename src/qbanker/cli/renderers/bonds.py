from __future__ import annotations

from rich.console import Console
from rich.table import Table

from qbanker.models.bonds import (
    BondPriceResult,
    BondYtmResult,
    BondDurationResult,
    BondConvexityResult,
    BondLadderResult,
)


def _simple_table(title: str, rows: list[tuple[str, str]]) -> None:
    table = Table(title=title)
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    for label, value in rows:
        table.add_row(label, value)
    Console().print(table)


def render_bond_price(result: BondPriceResult) -> None:
    _simple_table("Bond Price", [("Price", f"{result.price:,.2f}")])


def render_bond_ytm(result: BondYtmResult) -> None:
    _simple_table("Bond YTM", [("Yield", f"{result.yield_rate:.4f}%")])


def render_bond_duration(result: BondDurationResult) -> None:
    _simple_table(
        "Bond Duration",
        [
            ("Macaulay", f"{result.macaulay_duration:.4f}"),
            ("Modified", f"{result.modified_duration:.4f}"),
        ],
    )


def render_bond_convexity(result: BondConvexityResult) -> None:
    _simple_table("Bond Convexity", [("Convexity", f"{result.convexity:.6f}")])


def render_bond_ladder(result: BondLadderResult) -> None:
    table = Table(title="Bond Ladder")
    table.add_column("Maturity (years)", justify="right")
    table.add_column("Amount", justify="right")
    for maturity, amount in result.schedule:
        table.add_row(str(maturity), f"{amount:,.2f}")
    Console().print(table)

    _simple_table(
        "Ladder Summary",
        [
            ("Total Invested", f"{result.total_invested:,.2f}"),
            ("Weighted Maturity", f"{result.weighted_maturity:.2f}"),
        ],
    )
