from __future__ import annotations

import json
import typer

from qfinancetools.core.timeline import build_unified_timeline
from qfinancetools.models.bonds import BondPriceInput
from qfinancetools.models.investments import InvestmentInput
from qfinancetools.models.loans import LoanInput
from qfinancetools.models.stocks import StockProjectionInput
from qfinancetools.models.timeline import TimelineRequest
from qfinancetools.cli.renderers.timeline import render_timeline


def timeline_command(
    months: int = typer.Option(..., "--months"),
    include_loan: bool = typer.Option(True, "--include-loan/--no-include-loan"),
    loan_amount: float = typer.Option(350000, "--loan-amount"),
    loan_rate: float = typer.Option(5.4, "--loan-rate"),
    loan_years: int = typer.Option(25, "--loan-years"),
    loan_extra: float = typer.Option(0.0, "--loan-extra"),
    include_invest: bool = typer.Option(True, "--include-invest/--no-include-invest"),
    invest_initial: float = typer.Option(10000, "--invest-initial"),
    invest_monthly: float = typer.Option(500, "--invest-monthly"),
    invest_rate: float = typer.Option(7.0, "--invest-rate"),
    invest_years: int = typer.Option(20, "--invest-years"),
    include_bonds: bool = typer.Option(True, "--include-bonds/--no-include-bonds"),
    bond_face: float = typer.Option(1000, "--bond-face"),
    bond_coupon: float = typer.Option(5.0, "--bond-coupon"),
    bond_yield: float = typer.Option(4.5, "--bond-yield"),
    bond_years: int = typer.Option(10, "--bond-years"),
    bond_freq: int = typer.Option(2, "--bond-freq"),
    include_stocks: bool = typer.Option(True, "--include-stocks/--no-include-stocks"),
    stock_ticker: str = typer.Option("SPY", "--stock-ticker"),
    stock_initial: float = typer.Option(5000, "--stock-initial"),
    stock_monthly: float = typer.Option(300, "--stock-monthly"),
    stock_rate: float = typer.Option(8.0, "--stock-rate"),
    stock_years: int = typer.Option(20, "--stock-years"),
    stock_expense_ratio: float = typer.Option(0.03, "--stock-expense-ratio"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    request = TimelineRequest(
        months=months,
        include_loan=include_loan,
        include_invest=include_invest,
        include_bonds=include_bonds,
        include_stocks=include_stocks,
    )
    loan_input = LoanInput(principal=loan_amount, annual_rate=loan_rate, years=loan_years, extra_payment=loan_extra)
    invest_input = InvestmentInput(initial=invest_initial, monthly=invest_monthly, annual_rate=invest_rate, years=invest_years)
    bond_input = BondPriceInput(
        face_value=bond_face,
        coupon_rate=bond_coupon,
        yield_rate=bond_yield,
        years=bond_years,
        payments_per_year=bond_freq,
    )
    stock_input = StockProjectionInput(
        ticker=stock_ticker,
        initial=stock_initial,
        monthly=stock_monthly,
        annual_return=stock_rate,
        years=stock_years,
        expense_ratio=stock_expense_ratio,
    )
    result = build_unified_timeline(
        request,
        loan_input=loan_input if include_loan else None,
        invest_input=invest_input if include_invest else None,
        bond_input=bond_input if include_bonds else None,
        stock_input=stock_input if include_stocks else None,
    )
    if as_json:
        typer.echo(json.dumps(result.model_dump(), indent=2))
        return
    render_timeline(result)
