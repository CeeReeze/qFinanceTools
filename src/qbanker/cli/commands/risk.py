from __future__ import annotations

import json
import typer

from qbanker.core.risk import scenario, sensitivity, monte_carlo, stress_test
from qbanker.models.risk import (
    ScenarioInput,
    SensitivityInput,
    MonteCarloInput,
    StressTestInput,
)
from qbanker.cli.renderers.risk import (
    render_scenario,
    render_sensitivity,
    render_monte_carlo,
    render_stress_test,
)
from qbanker.cli.prompts import prompt_float, prompt_int, prompt_list_float


risk_app = typer.Typer(no_args_is_help=True)


@risk_app.command("scenario")
def scenario_command(
    base: float | None = typer.Option(None, "--base", help="Base value."),
    shocks: list[float] | None = typer.Option(None, "--shock", help="Shock (percent, repeatable)."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        base = prompt_float("Base value", base)
        shocks = prompt_list_float("Shocks (%) (comma or space separated)")
    if base is None or not shocks:
        raise typer.BadParameter("--base and --shock are required unless --interactive is used")

    data = ScenarioInput(base_value=base, shocks=shocks)
    result = scenario(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_scenario(result)


@risk_app.command("sensitivity")
def sensitivity_command(
    base: float | None = typer.Option(None, "--base", help="Base value."),
    change: float | None = typer.Option(None, "--change", help="Percent change."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        base = prompt_float("Base value", base)
        change = prompt_float("Percent change", change)
    if base is None or change is None:
        raise typer.BadParameter("--base and --change are required unless --interactive is used")

    data = SensitivityInput(base_value=base, change=change)
    result = sensitivity(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_sensitivity(result)


@risk_app.command("montecarlo")
def monte_carlo_command(
    initial: float | None = typer.Option(None, "--initial", help="Initial value."),
    mean: float | None = typer.Option(None, "--mean", help="Mean return (percent)."),
    volatility: float | None = typer.Option(None, "--volatility", help="Volatility (percent)."),
    years: int | None = typer.Option(None, "--years", help="Years to simulate."),
    simulations: int | None = typer.Option(None, "--sims", help="Number of simulations."),
    seed: int = typer.Option(0, "--seed", help="Random seed."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        initial = prompt_float("Initial value", initial)
        mean = prompt_float("Mean return (%)", mean)
        volatility = prompt_float("Volatility (%)", volatility)
        years = prompt_int("Years to simulate", years)
        simulations = prompt_int("Number of simulations", simulations)
        seed = prompt_int("Random seed", seed)
    if initial is None or mean is None or volatility is None or years is None or simulations is None:
        raise typer.BadParameter("--initial, --mean, --volatility, --years, and --sims are required unless --interactive is used")

    data = MonteCarloInput(
        initial_value=initial,
        mean_return=mean,
        volatility=volatility,
        years=years,
        simulations=simulations,
        seed=seed,
    )
    result = monte_carlo(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_monte_carlo(result)


@risk_app.command("stress-test")
def stress_test_command(
    base: float | None = typer.Option(None, "--base", help="Base value."),
    drawdown: float | None = typer.Option(None, "--drawdown", help="Drawdown (0-1)."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        base = prompt_float("Base value", base)
        drawdown = prompt_float("Drawdown (0-1)", drawdown)
    if base is None or drawdown is None:
        raise typer.BadParameter("--base and --drawdown are required unless --interactive is used")

    data = StressTestInput(base_value=base, drawdown=drawdown)
    result = stress_test(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_stress_test(result)
