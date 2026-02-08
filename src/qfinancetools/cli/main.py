from __future__ import annotations

import importlib.metadata
import typer

from qfinancetools.cli.commands import loan, invest, afford, corporate, bonds, risk

app = typer.Typer(no_args_is_help=True)


@app.callback()
def _version_callback(
    version: bool = typer.Option(
        False,
        "--version",
        help="Show the qfin version and exit.",
        is_eager=True,
    )
) -> None:
    if version:
        typer.echo(importlib.metadata.version("qfinance"))
        raise typer.Exit()


app.command("loan")(loan.loan_command)
app.command("invest")(invest.invest_command)
app.command("afford")(afford.afford_command)
app.add_typer(corporate.corporate_app, name="corporate")
app.add_typer(bonds.bonds_app, name="bonds")
app.add_typer(risk.risk_app, name="risk")
