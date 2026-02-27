import datetime as dt

import pytest

import qfinancetools.core.stocks as stocks_core
from qfinancetools.core.stocks import stock_backtest, stock_history, stock_projection
from qfinancetools.models.stocks import (
    StockBacktestInput,
    StockHistoryInput,
    StockProjectionInput,
)


def test_stock_projection_basic() -> None:
    result = stock_projection(
        StockProjectionInput(
            ticker="VOO",
            initial=1000,
            monthly=100,
            annual_return=12,
            years=1,
            expense_ratio=0.03,
        )
    )
    assert result.ticker == "VOO"
    assert result.final_value > result.total_contributions
    assert result.effective_annual_return == 11.97


def test_stock_history_group_series(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch(ticker: str, start: dt.date, end: dt.date) -> list[tuple[dt.date, float]]:
        _ = start, end
        if ticker == "AAA":
            return [
                (dt.date(2024, 1, 2), 100.0),
                (dt.date(2024, 2, 2), 110.0),
                (dt.date(2024, 3, 2), 120.0),
            ]
        return [
            (dt.date(2024, 1, 2), 50.0),
            (dt.date(2024, 2, 2), 55.0),
            (dt.date(2024, 3, 2), 57.5),
        ]

    monkeypatch.setattr(stocks_core, "_fetch_history_yahoo", fake_fetch)
    result = stock_history(
        StockHistoryInput(
            tickers=["AAA", "BBB"],
            start_date="2024-01-01",
            end_date="2024-03-10",
            weights=[0.5, 0.5],
        )
    )
    assert len(result.series) == 3
    portfolio = next(item for item in result.series if item.name == "PORTFOLIO")
    assert portfolio.points[0].normalized == pytest.approx(100.0)
    assert portfolio.points[-1].normalized > 110.0


def test_stock_backtest_lump_and_periodic(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch(ticker: str, start: dt.date, end: dt.date) -> list[tuple[dt.date, float]]:
        _ = ticker, start, end
        return [
            (dt.date(2024, 1, 2), 100.0),
            (dt.date(2024, 2, 1), 105.0),
            (dt.date(2024, 3, 1), 110.0),
        ]

    monkeypatch.setattr(stocks_core, "_fetch_history_yahoo", fake_fetch)
    result = stock_backtest(
        StockBacktestInput(
            tickers=["AAA"],
            start_date="2024-01-01",
            end_date="2024-03-10",
            lump_sum=1000,
            periodic_amount=100,
            periodic_months=1,
        )
    )
    assert result.final_invested == pytest.approx(1300)
    assert result.final_value > result.final_invested


def test_stock_history_uses_cache_on_fetch_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_fetch(ticker: str, start: dt.date, end: dt.date) -> list[tuple[dt.date, float]]:
        _ = ticker, start, end
        raise ValueError("HTTP Error 429: Too Many Requests")

    def fake_cached(
        ticker: str, start: dt.date, end: dt.date
    ) -> tuple[list[tuple[dt.date, float]] | None, dt.date | None]:
        _ = ticker, start, end
        return (
            [
                (dt.date(2024, 1, 2), 100.0),
                (dt.date(2024, 2, 2), 110.0),
            ],
            dt.date(2024, 2, 3),
        )

    monkeypatch.setattr(stocks_core, "_fetch_history_yahoo", fail_fetch)
    monkeypatch.setattr(stocks_core, "_load_cached_history", fake_cached)
    monkeypatch.setattr(stocks_core, "_save_cached_history", lambda *args, **kwargs: None)

    result = stock_history(
        StockHistoryInput(
            tickers=["AAA"],
            start_date="2024-01-01",
            end_date="2024-02-10",
        )
    )
    assert len(result.series) == 2
    assert any(item.code == "stocks.cache_fallback" for item in result.warnings)
