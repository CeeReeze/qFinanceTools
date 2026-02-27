from __future__ import annotations

import json
import typer

from qfinancetools.core.goals import solve_investment_goal, solve_loan_payoff_goal
from qfinancetools.models.goals import InvestmentGoalInput, LoanPayoffGoalInput
from qfinancetools.cli.renderers.goals import render_investment_goal, render_loan_goal


goal_app = typer.Typer(no_args_is_help=True)


@goal_app.command("invest")
def goal_invest(
    target: float = typer.Option(..., "--target"),
    initial: float = typer.Option(..., "--initial"),
    years: int = typer.Option(..., "--years"),
    monthly: float | None = typer.Option(None, "--monthly"),
    rate: float | None = typer.Option(None, "--rate"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    data = InvestmentGoalInput(
        target_value=target,
        initial=initial,
        years=years,
        monthly=monthly,
        annual_rate=rate,
    )
    result = solve_investment_goal(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_investment_goal(result)


@goal_app.command("loan-payoff")
def goal_loan_payoff(
    principal: float = typer.Option(..., "--principal"),
    rate: float = typer.Option(..., "--rate"),
    current_years: int = typer.Option(..., "--current-years"),
    target_years: int = typer.Option(..., "--target-years"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    data = LoanPayoffGoalInput(
        principal=principal,
        annual_rate=rate,
        current_years=current_years,
        target_years=target_years,
    )
    result = solve_loan_payoff_goal(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_loan_goal(result)
