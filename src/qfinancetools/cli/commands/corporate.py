from __future__ import annotations

import json
import typer

from qfinancetools.core.corporate import wacc, capm, npv, irr, dcf, comps
from qfinancetools.models.corporate import (
    WaccInput,
    CapmInput,
    NpvInput,
    IrrInput,
    DcfInput,
    CompsInput,
)
from qfinancetools.cli.renderers.corporate import (
    render_wacc,
    render_capm,
    render_npv,
    render_irr,
    render_dcf,
    render_comps,
)
from qfinancetools.cli.prompts import (
    prompt_float,
    prompt_list_float,
    prompt_optional_float,
)


corporate_app = typer.Typer(no_args_is_help=True)


@corporate_app.command("wacc")
def wacc_command(
    cost_of_equity: float | None = typer.Option(None, "--equity", help="Cost of equity (percent)."),
    cost_of_debt: float | None = typer.Option(None, "--debt", help="Cost of debt (percent)."),
    tax_rate: float | None = typer.Option(None, "--tax", help="Tax rate (0-1)."),
    equity_value: float | None = typer.Option(None, "--equity-value", help="Market value of equity."),
    debt_value: float | None = typer.Option(None, "--debt-value", help="Market value of debt."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        cost_of_equity = prompt_float("Cost of equity (%)", cost_of_equity)
        cost_of_debt = prompt_float("Cost of debt (%)", cost_of_debt)
        tax_rate = prompt_float("Tax rate (0-1)", tax_rate)
        equity_value = prompt_float("Market value of equity", equity_value)
        debt_value = prompt_float("Market value of debt", debt_value)
    if (
        cost_of_equity is None
        or cost_of_debt is None
        or tax_rate is None
        or equity_value is None
        or debt_value is None
    ):
        raise typer.BadParameter("--equity, --debt, --tax, --equity-value, and --debt-value are required unless --interactive is used")

    data = WaccInput(
        cost_of_equity=cost_of_equity,
        cost_of_debt=cost_of_debt,
        tax_rate=tax_rate,
        equity_value=equity_value,
        debt_value=debt_value,
    )
    result = wacc(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_wacc(result)


@corporate_app.command("capm")
def capm_command(
    risk_free: float | None = typer.Option(None, "--rf", help="Risk-free rate (percent)."),
    beta: float | None = typer.Option(None, "--beta", help="Beta."),
    market_return: float | None = typer.Option(None, "--market", help="Market return (percent)."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        risk_free = prompt_float("Risk-free rate (%)", risk_free)
        beta = prompt_float("Beta", beta)
        market_return = prompt_float("Market return (%)", market_return)
    if risk_free is None or beta is None or market_return is None:
        raise typer.BadParameter("--rf, --beta, and --market are required unless --interactive is used")

    data = CapmInput(risk_free_rate=risk_free, beta=beta, market_return=market_return)
    result = capm(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_capm(result)


@corporate_app.command("npv")
def npv_command(
    rate: float | None = typer.Option(None, "--rate", help="Discount rate (percent)."),
    cash_flows: list[float] | None = typer.Option(None, "--cash-flow", help="Cash flow (repeatable)."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        rate = prompt_float("Discount rate (%)", rate)
        cash_flows = prompt_list_float("Cash flows (comma or space separated)")
    if rate is None or not cash_flows:
        raise typer.BadParameter("--rate and --cash-flow are required unless --interactive is used")

    data = NpvInput(discount_rate=rate, cash_flows=cash_flows)
    result = npv(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_npv(result)


@corporate_app.command("irr")
def irr_command(
    cash_flows: list[float] | None = typer.Option(None, "--cash-flow", help="Cash flow (repeatable)."),
    guess: float = typer.Option(0.1, "--guess", help="Initial guess (rate, decimal)."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        cash_flows = prompt_list_float("Cash flows (comma or space separated)")
        guess = prompt_float("Initial guess (decimal)", guess)
    if not cash_flows:
        raise typer.BadParameter("--cash-flow is required unless --interactive is used")

    data = IrrInput(cash_flows=cash_flows, guess=guess)
    result = irr(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_irr(result)


@corporate_app.command("dcf")
def dcf_command(
    rate: float | None = typer.Option(None, "--rate", help="Discount rate (percent)."),
    cash_flows: list[float] | None = typer.Option(None, "--cash-flow", help="Cash flow (repeatable)."),
    terminal_growth: float = typer.Option(0.0, "--terminal-growth", help="Terminal growth (decimal)."),
    terminal_multiple: float | None = typer.Option(None, "--terminal-multiple", help="Terminal multiple."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        rate = prompt_float("Discount rate (%)", rate)
        cash_flows = prompt_list_float("Cash flows (comma or space separated)")
        terminal_growth = prompt_float("Terminal growth (decimal)", terminal_growth)
        terminal_multiple = prompt_optional_float("Terminal multiple (optional)")
    if rate is None or not cash_flows:
        raise typer.BadParameter("--rate and --cash-flow are required unless --interactive is used")

    data = DcfInput(
        discount_rate=rate,
        cash_flows=cash_flows,
        terminal_growth=terminal_growth,
        terminal_multiple=terminal_multiple,
    )
    result = dcf(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_dcf(result)


@corporate_app.command("comps")
def comps_command(
    metric: float | None = typer.Option(None, "--metric", help="Metric value (e.g., EBITDA)."),
    multiples: list[float] | None = typer.Option(None, "--multiple", help="Comparable multiple (repeatable)."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        metric = prompt_float("Metric value", metric)
        multiples = prompt_list_float("Comparable multiples (comma or space separated)")
    if metric is None or not multiples:
        raise typer.BadParameter("--metric and --multiple are required unless --interactive is used")

    data = CompsInput(metric=metric, multiples=multiples)
    result = comps(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_comps(result)
