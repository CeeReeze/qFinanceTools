from __future__ import annotations

import json
import typer

from qfinancetools.core.comparison import compare_scenarios
from qfinancetools.models.comparison import ComparisonCase, ComparisonRequest
from qfinancetools.cli.renderers.comparison import render_comparison


compare_app = typer.Typer(no_args_is_help=True)


@compare_app.command("loan")
def compare_loan(
    base_amount: float = typer.Option(..., "--base-amount"),
    base_rate: float = typer.Option(..., "--base-rate"),
    base_years: int = typer.Option(..., "--base-years"),
    base_extra: float = typer.Option(0.0, "--base-extra"),
    alt_amount: float = typer.Option(..., "--alt-amount"),
    alt_rate: float = typer.Option(..., "--alt-rate"),
    alt_years: int = typer.Option(..., "--alt-years"),
    alt_extra: float = typer.Option(0.0, "--alt-extra"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    request = ComparisonRequest(
        calculator="loan",
        base=ComparisonCase(
            label="Base",
            inputs={"amount": base_amount, "rate": base_rate, "years": base_years, "extra": base_extra},
        ),
        alt=ComparisonCase(
            label="Alt",
            inputs={"amount": alt_amount, "rate": alt_rate, "years": alt_years, "extra": alt_extra},
        ),
    )
    result = compare_scenarios(request)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_comparison(result)


@compare_app.command("invest")
def compare_invest(
    base_initial: float = typer.Option(..., "--base-initial"),
    base_monthly: float = typer.Option(..., "--base-monthly"),
    base_rate: float = typer.Option(..., "--base-rate"),
    base_years: int = typer.Option(..., "--base-years"),
    alt_initial: float = typer.Option(..., "--alt-initial"),
    alt_monthly: float = typer.Option(..., "--alt-monthly"),
    alt_rate: float = typer.Option(..., "--alt-rate"),
    alt_years: int = typer.Option(..., "--alt-years"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    request = ComparisonRequest(
        calculator="invest",
        base=ComparisonCase(
            label="Base",
            inputs={
                "initial": base_initial,
                "monthly": base_monthly,
                "rate": base_rate,
                "years": base_years,
            },
        ),
        alt=ComparisonCase(
            label="Alt",
            inputs={
                "initial": alt_initial,
                "monthly": alt_monthly,
                "rate": alt_rate,
                "years": alt_years,
            },
        ),
    )
    result = compare_scenarios(request)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_comparison(result)


@compare_app.command("risk")
def compare_risk(
    base_initial: float = typer.Option(..., "--base-initial"),
    base_mean: float = typer.Option(..., "--base-mean"),
    base_volatility: float = typer.Option(..., "--base-volatility"),
    base_years: int = typer.Option(..., "--base-years"),
    base_sims: int = typer.Option(..., "--base-sims"),
    alt_initial: float = typer.Option(..., "--alt-initial"),
    alt_mean: float = typer.Option(..., "--alt-mean"),
    alt_volatility: float = typer.Option(..., "--alt-volatility"),
    alt_years: int = typer.Option(..., "--alt-years"),
    alt_sims: int = typer.Option(..., "--alt-sims"),
    seed: int = typer.Option(42, "--seed"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    request = ComparisonRequest(
        calculator="risk",
        base=ComparisonCase(
            label="Base",
            inputs={
                "initial": base_initial,
                "mean": base_mean,
                "volatility": base_volatility,
                "years": base_years,
                "sims": base_sims,
                "seed": seed,
            },
        ),
        alt=ComparisonCase(
            label="Alt",
            inputs={
                "initial": alt_initial,
                "mean": alt_mean,
                "volatility": alt_volatility,
                "years": alt_years,
                "sims": alt_sims,
                "seed": seed,
            },
        ),
    )
    result = compare_scenarios(request)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_comparison(result)
