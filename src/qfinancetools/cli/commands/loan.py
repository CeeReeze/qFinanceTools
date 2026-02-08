from __future__ import annotations

import json
import typer

from qfinancetools.core.loans import amortization_schedule, loan_summary
from qfinancetools.models.loans import LoanInput
from qfinancetools.cli.renderers.loan import render_loan_summary, render_amortization
from qfinancetools.cli.prompts import prompt_float, prompt_int, prompt_bool


def loan_command(
    amount: float | None = typer.Option(None, "--amount", help="Loan principal."),
    rate: float | None = typer.Option(None, "--rate", help="Annual interest rate (percent)."),
    years: int | None = typer.Option(None, "--years", help="Loan term in years."),
    extra: float = typer.Option(0.0, "--extra", help="Extra monthly payment."),
    schedule: bool = typer.Option(False, "--schedule", help="Show amortization schedule."),
    interactive: bool = typer.Option(False, "--interactive", help="Prompt for inputs."),
    as_json: bool = typer.Option(False, "--json", help="Output JSON only."),
) -> None:
    if interactive:
        amount = prompt_float("Loan principal", amount)
        rate = prompt_float("Annual interest rate (%)", rate)
        years = prompt_int("Loan term (years)", years)
        extra = prompt_float("Extra monthly payment", extra)
        schedule = prompt_bool("Show amortization schedule", schedule)
    if amount is None or rate is None or years is None:
        raise typer.BadParameter("--amount, --rate, and --years are required unless --interactive is used")

    data = LoanInput(
        principal=amount,
        annual_rate=rate,
        years=years,
        extra_payment=extra,
    )
    summary = loan_summary(data)

    if as_json:
        payload = {"summary": summary.model_dump()}
        if schedule:
            rows = amortization_schedule(data)
            payload["schedule"] = [row.model_dump() for row in rows]
        typer.echo(json.dumps(payload, indent=2))
        return

    render_loan_summary(summary)
    if schedule:
        rows = amortization_schedule(data)
        render_amortization(rows)
