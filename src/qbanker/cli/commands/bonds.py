from __future__ import annotations

import json
import typer

from qbanker.core.bonds import (
    bond_price,
    bond_ytm,
    bond_duration,
    bond_convexity,
    bond_ladder,
)
from qbanker.models.bonds import (
    BondPriceInput,
    BondYtmInput,
    BondDurationInput,
    BondConvexityInput,
    BondLadderInput,
)
from qbanker.cli.renderers.bonds import (
    render_bond_price,
    render_bond_ytm,
    render_bond_duration,
    render_bond_convexity,
    render_bond_ladder,
)
from qbanker.cli.prompts import prompt_float, prompt_int, prompt_list_int, prompt_list_float


bonds_app = typer.Typer(no_args_is_help=True)


@bonds_app.command("price")
def price_command(
    face: float | None = typer.Option(None, "--face", help="Face value."),
    coupon: float | None = typer.Option(None, "--coupon", help="Coupon rate (percent)."),
    ytm: float | None = typer.Option(None, "--ytm", help="Yield to maturity (percent)."),
    years: int | None = typer.Option(None, "--years", help="Years to maturity."),
    freq: int = typer.Option(2, "--freq", help="Payments per year."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        face = prompt_float("Face value", face)
        coupon = prompt_float("Coupon rate (%)", coupon)
        ytm = prompt_float("Yield to maturity (%)", ytm)
        years = prompt_int("Years to maturity", years)
        freq = prompt_int("Payments per year", freq)
    if face is None or coupon is None or ytm is None or years is None:
        raise typer.BadParameter("--face, --coupon, --ytm, and --years are required unless --interactive is used")

    data = BondPriceInput(
        face_value=face,
        coupon_rate=coupon,
        yield_rate=ytm,
        years=years,
        payments_per_year=freq,
    )
    result = bond_price(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_bond_price(result)


@bonds_app.command("ytm")
def ytm_command(
    face: float | None = typer.Option(None, "--face", help="Face value."),
    coupon: float | None = typer.Option(None, "--coupon", help="Coupon rate (percent)."),
    price: float | None = typer.Option(None, "--price", help="Bond price."),
    years: int | None = typer.Option(None, "--years", help="Years to maturity."),
    freq: int = typer.Option(2, "--freq", help="Payments per year."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        face = prompt_float("Face value", face)
        coupon = prompt_float("Coupon rate (%)", coupon)
        price = prompt_float("Bond price", price)
        years = prompt_int("Years to maturity", years)
        freq = prompt_int("Payments per year", freq)
    if face is None or coupon is None or price is None or years is None:
        raise typer.BadParameter("--face, --coupon, --price, and --years are required unless --interactive is used")

    data = BondYtmInput(
        face_value=face,
        coupon_rate=coupon,
        price=price,
        years=years,
        payments_per_year=freq,
    )
    result = bond_ytm(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_bond_ytm(result)


@bonds_app.command("duration")
def duration_command(
    face: float | None = typer.Option(None, "--face", help="Face value."),
    coupon: float | None = typer.Option(None, "--coupon", help="Coupon rate (percent)."),
    ytm: float | None = typer.Option(None, "--ytm", help="Yield to maturity (percent)."),
    years: int | None = typer.Option(None, "--years", help="Years to maturity."),
    freq: int = typer.Option(2, "--freq", help="Payments per year."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        face = prompt_float("Face value", face)
        coupon = prompt_float("Coupon rate (%)", coupon)
        ytm = prompt_float("Yield to maturity (%)", ytm)
        years = prompt_int("Years to maturity", years)
        freq = prompt_int("Payments per year", freq)
    if face is None or coupon is None or ytm is None or years is None:
        raise typer.BadParameter("--face, --coupon, --ytm, and --years are required unless --interactive is used")

    data = BondDurationInput(
        face_value=face,
        coupon_rate=coupon,
        yield_rate=ytm,
        years=years,
        payments_per_year=freq,
    )
    result = bond_duration(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_bond_duration(result)


@bonds_app.command("convexity")
def convexity_command(
    face: float | None = typer.Option(None, "--face", help="Face value."),
    coupon: float | None = typer.Option(None, "--coupon", help="Coupon rate (percent)."),
    ytm: float | None = typer.Option(None, "--ytm", help="Yield to maturity (percent)."),
    years: int | None = typer.Option(None, "--years", help="Years to maturity."),
    freq: int = typer.Option(2, "--freq", help="Payments per year."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        face = prompt_float("Face value", face)
        coupon = prompt_float("Coupon rate (%)", coupon)
        ytm = prompt_float("Yield to maturity (%)", ytm)
        years = prompt_int("Years to maturity", years)
        freq = prompt_int("Payments per year", freq)
    if face is None or coupon is None or ytm is None or years is None:
        raise typer.BadParameter("--face, --coupon, --ytm, and --years are required unless --interactive is used")

    data = BondConvexityInput(
        face_value=face,
        coupon_rate=coupon,
        yield_rate=ytm,
        years=years,
        payments_per_year=freq,
    )
    result = bond_convexity(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_bond_convexity(result)


@bonds_app.command("ladder")
def ladder_command(
    maturities: list[int] | None = typer.Option(None, "--maturity", help="Maturity in years (repeatable)."),
    amounts: list[float] | None = typer.Option(None, "--amount", help="Amount per rung (repeatable)."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    if interactive:
        maturities = prompt_list_int("Maturities (years, comma or space separated)")
        amounts = prompt_list_float("Amounts (comma or space separated)")
    if not maturities or not amounts:
        raise typer.BadParameter("--maturity and --amount are required unless --interactive is used")

    data = BondLadderInput(maturities=maturities, amounts=amounts)
    result = bond_ladder(data)
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_bond_ladder(result)
