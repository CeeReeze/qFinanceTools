from __future__ import annotations

from rich.console import Console
from rich.table import Table

from qfinancetools.models.corporate import (
    WaccResult,
    CapmResult,
    NpvResult,
    IrrResult,
    DcfResult,
    CompsResult,
)


def _simple_table(title: str, rows: list[tuple[str, str]]) -> None:
    table = Table(title=title)
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    for label, value in rows:
        table.add_row(label, value)
    Console().print(table)


def render_wacc(result: WaccResult) -> None:
    _simple_table("WACC", [("WACC", f"{result.wacc:.4f}%")])


def render_capm(result: CapmResult) -> None:
    _simple_table("CAPM", [("Cost of Equity", f"{result.cost_of_equity:.4f}%")])


def render_npv(result: NpvResult) -> None:
    _simple_table("NPV", [("Net Present Value", f"{result.npv:,.2f}")])


def render_irr(result: IrrResult) -> None:
    _simple_table("IRR", [("IRR", f"{result.irr:.4f}%")])


def render_dcf(result: DcfResult) -> None:
    _simple_table(
        "DCF",
        [
            ("Present Value", f"{result.present_value:,.2f}"),
            ("Terminal Value", f"{result.terminal_value:,.2f}"),
            ("Total Value", f"{result.total_value:,.2f}"),
        ],
    )


def render_comps(result: CompsResult) -> None:
    _simple_table(
        "Comps",
        [
            ("Low", f"{result.low:,.2f}"),
            ("Median", f"{result.median:,.2f}"),
            ("High", f"{result.high:,.2f}"),
        ],
    )
