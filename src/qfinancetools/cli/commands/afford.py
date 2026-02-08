from __future__ import annotations

import json
import typer

from qfinancetools.core.afford import affordability
from qfinancetools.models.afford import AffordInput
from qfinancetools.cli.renderers.afford import render_affordability
from qfinancetools.cli.prompts import prompt_float


def afford_command(
    income: float | None = typer.Option(None, "--income", help="Monthly income."),
    debts: float | None = typer.Option(None, "--debts", help="Monthly debt payments."),
    housing: float | None = typer.Option(None, "--housing", help="Monthly housing cost."),
    max_dti: float | None = typer.Option(None, "--max-dti", help="Max DTI ratio (0-1)."),
    stress_rate: float = typer.Option(
        0.0,
        "--stress-rate",
        help="Stress rate as percent applied to housing cost.",
    ),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json", help="Output JSON only."),
) -> None:
    if interactive:
        income = prompt_float("Monthly income", income)
        debts = prompt_float("Monthly debt payments", debts)
        housing = prompt_float("Monthly housing cost", housing)
        max_dti = prompt_float("Max DTI ratio (0-1)", max_dti)
        stress_rate = prompt_float("Stress rate (%)", stress_rate)
    if income is None or debts is None or housing is None or max_dti is None:
        raise typer.BadParameter("--income, --debts, --housing, and --max-dti are required unless --interactive is used")

    data = AffordInput(
        income_monthly=income,
        debts_monthly=debts,
        housing_cost=housing,
        max_dti=max_dti,
        stress_rate=stress_rate,
    )
    result = affordability(data)

    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return

    render_affordability(result)
