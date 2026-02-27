from __future__ import annotations

import json
import typer

from qfinancetools.core.stocks import stock_backtest, stock_history, stock_projection
from qfinancetools.models.stocks import (
    StockBacktestInput,
    StockHistoryInput,
    StockProjectionInput,
)
from qfinancetools.cli.renderers.stocks import (
    render_stock_backtest,
    render_stock_history,
    render_stock_projection,
)


def stocks_command(
    mode: str = typer.Option(
        "projection",
        "--mode",
        help="Mode: projection | history | backtest.",
    ),
    ticker: list[str] = typer.Option(..., "--ticker", help="Ticker(s). Repeat for groups."),
    weight: list[float] | None = typer.Option(None, "--weight", help="Optional portfolio weights."),
    initial: float = typer.Option(0.0, "--initial", help="Initial investment (projection)."),
    monthly: float = typer.Option(0.0, "--monthly", help="Monthly contribution (projection)."),
    rate: float = typer.Option(0.0, "--rate", help="Expected annual return rate (projection)."),
    years: int = typer.Option(1, "--years", help="Projection horizon in years."),
    expense_ratio: float = typer.Option(0.0, "--expense-ratio", help="ETF/strategy expense ratio (percent)."),
    start_date: str | None = typer.Option(None, "--start-date", help="Backtest/history start date YYYY-MM-DD."),
    end_date: str | None = typer.Option(None, "--end-date", help="Backtest/history end date YYYY-MM-DD."),
    period_years: int = typer.Option(5, "--period-years", help="If start-date omitted, look back this many years."),
    lump_sum: float = typer.Option(0.0, "--lump-sum", help="One-time investment at start (backtest)."),
    periodic_amount: float = typer.Option(0.0, "--periodic-amount", help="Recurring contribution amount (backtest)."),
    periodic_months: int = typer.Option(1, "--periodic-months", help="Recurring contribution period in months."),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    normalized_mode = mode.strip().lower()
    if normalized_mode == "projection":
        if len(ticker) != 1:
            raise typer.BadParameter("projection mode requires exactly one --ticker")
        data = StockProjectionInput(
            ticker=ticker[0],
            initial=initial,
            monthly=monthly,
            annual_return=rate,
            years=years,
            expense_ratio=expense_ratio,
        )
        result = stock_projection(data)
        if as_json:
            typer.echo(json.dumps(result.model_dump(), indent=2))
            return
        render_stock_projection(result)
        return

    if normalized_mode == "history":
        data = StockHistoryInput(
            tickers=ticker,
            start_date=start_date,
            end_date=end_date,
            period_years=period_years,
            weights=weight,
        )
        result = stock_history(data)
        if as_json:
            typer.echo(json.dumps(result.model_dump(), indent=2))
            return
        render_stock_history(result)
        return

    if normalized_mode == "backtest":
        data = StockBacktestInput(
            tickers=ticker,
            start_date=start_date,
            end_date=end_date,
            period_years=period_years,
            lump_sum=lump_sum,
            periodic_amount=periodic_amount,
            periodic_months=periodic_months,
            weights=weight,
        )
        result = stock_backtest(data)
        if as_json:
            typer.echo(json.dumps(result.model_dump(), indent=2))
            return
        render_stock_backtest(result)
        return

    raise typer.BadParameter("--mode must be one of: projection, history, backtest")
