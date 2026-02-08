import json

from typer.testing import CliRunner

from qbanker.cli.main import app


runner = CliRunner()


def test_cli_loan_json() -> None:
    result = runner.invoke(
        app,
        [
            "loan",
            "--amount",
            "100000",
            "--rate",
            "6",
            "--years",
            "30",
            "--json",
        ],
    )
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert "summary" in payload
    assert "monthly_payment" in payload["summary"]
