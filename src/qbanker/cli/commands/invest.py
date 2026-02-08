from __future__ import annotations

import json
import typer

from qbanker.core.investments import investment_growth
from qbanker.models.investments import InvestmentInput
from qbanker.cli.renderers.invest import render_investment_summary
from qbanker.cli.prompts import prompt_float, prompt_int


def invest_command(
    initial: float | None = typer.Option(None, "--initial", help="Initial investment."),
    monthly: float | None = typer.Option(None, "--monthly", help="Monthly contribution."),
    rate: float | None = typer.Option(None, "--rate", help="Annual return rate (percent)."),
    years: int | None = typer.Option(None, "--years", help="Investment horizon in years."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json", help="Output JSON only."),
) -> None:
    if interactive:
        initial = prompt_float("Initial investment", initial)
        monthly = prompt_float("Monthly contribution", monthly)
        rate = prompt_float("Annual return rate (%)", rate)
        years = prompt_int("Investment horizon (years)", years)
    if initial is None or monthly is None or rate is None or years is None:
        raise typer.BadParameter("--initial, --monthly, --rate, and --years are required unless --interactive is used")

    data = InvestmentInput(
        initial=initial,
        monthly=monthly,
        annual_rate=rate,
        years=years,
    )
    result = investment_growth(data)

    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return

    render_investment_summary(result)
