import json
import datetime as dt

from typer.testing import CliRunner

from qfinancetools.cli.main import app
import qfinancetools.core.stocks as stocks_core


runner = CliRunner()


def test_cli_compare_loan_json() -> None:
    result = runner.invoke(
        app,
        [
            "compare",
            "loan",
            "--base-amount",
            "300000",
            "--base-rate",
            "5.4",
            "--base-years",
            "25",
            "--alt-amount",
            "300000",
            "--alt-rate",
            "4.8",
            "--alt-years",
            "25",
            "--json",
        ],
    )
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["calculator"] == "loan"


def test_cli_goal_invest_json() -> None:
    result = runner.invoke(
        app,
        [
            "goal",
            "invest",
            "--target",
            "500000",
            "--initial",
            "50000",
            "--years",
            "20",
            "--rate",
            "7",
            "--json",
        ],
    )
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert "required_monthly" in payload


def test_cli_stocks_json() -> None:
    result = runner.invoke(
        app,
        [
            "stocks",
            "--ticker",
            "VOO",
            "--initial",
            "10000",
            "--monthly",
            "300",
            "--rate",
            "8",
            "--years",
            "20",
            "--json",
        ],
    )
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ticker"] == "VOO"


def test_cli_stocks_history_json(monkeypatch) -> None:
    def fake_fetch(ticker: str, start: dt.date, end: dt.date) -> list[tuple[dt.date, float]]:
        _ = ticker, start, end
        return [
            (dt.date(2024, 1, 2), 100.0),
            (dt.date(2024, 2, 2), 110.0),
        ]

    monkeypatch.setattr(stocks_core, "_fetch_history_yahoo", fake_fetch)
    result = runner.invoke(
        app,
        [
            "stocks",
            "--mode",
            "history",
            "--ticker",
            "VOO",
            "--start-date",
            "2024-01-01",
            "--end-date",
            "2024-02-10",
            "--json",
        ],
    )
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["source"] == "yahoo_chart"
    assert payload["series"][0]["name"] == "VOO"
