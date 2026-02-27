from __future__ import annotations

from rich.console import Console
from rich.table import Table

from qfinancetools.models.risk import (
    ScenarioResult,
    SensitivityResult,
    MonteCarloResult,
    StressTestResult,
)


def _simple_table(title: str, rows: list[tuple[str, str]]) -> None:
    table = Table(title=title)
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    for label, value in rows:
        table.add_row(label, value)
    Console().print(table)


def _render_explain_and_warnings(warnings, explanation) -> None:
    if warnings:
        warn = Table(title="Warnings")
        warn.add_column("Code")
        warn.add_column("Message")
        for item in warnings:
            warn.add_row(item.code, item.message)
        Console().print(warn)
    if explanation:
        explain = Table(title="Explanation")
        explain.add_column("Step")
        explain.add_column("Formula")
        explain.add_column("Value", justify="right")
        for step in explanation.steps:
            value = f"{step.value:,.6f}" if isinstance(step.value, float) else str(step.value)
            explain.add_row(step.name, step.formula, value)
        Console().print(explain)


def render_scenario(result: ScenarioResult) -> None:
    table = Table(title="Scenario Outcomes")
    table.add_column("Scenario", justify="right")
    table.add_column("Outcome", justify="right")
    for idx, value in enumerate(result.outcomes, start=1):
        table.add_row(str(idx), f"{value:,.2f}")
    Console().print(table)
    _render_explain_and_warnings(result.warnings, result.explanation)


def render_sensitivity(result: SensitivityResult) -> None:
    _simple_table(
        "Sensitivity",
        [
            ("New Value", f"{result.new_value:,.2f}"),
            ("Percent Change", f"{result.percent_change:.4f}"),
        ],
    )
    _render_explain_and_warnings(result.warnings, result.explanation)


def render_monte_carlo(result: MonteCarloResult) -> None:
    _simple_table(
        "Monte Carlo",
        [
            ("Mean", f"{result.mean:,.2f}"),
            ("Median", f"{result.median:,.2f}"),
            ("P5", f"{result.p5:,.2f}"),
            ("P95", f"{result.p95:,.2f}"),
        ],
    )
    _render_explain_and_warnings(result.warnings, result.explanation)


def render_stress_test(result: StressTestResult) -> None:
    _simple_table("Stress Test", [("Stressed Value", f"{result.stressed_value:,.2f}")])
    _render_explain_and_warnings(result.warnings, result.explanation)
