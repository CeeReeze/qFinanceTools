import pytest

from qfinancetools.core.corporate import wacc, capm, npv, irr, dcf, comps
from qfinancetools.models.corporate import (
    WaccInput,
    CapmInput,
    NpvInput,
    IrrInput,
    DcfInput,
    CompsInput,
)


def test_wacc() -> None:
    data = WaccInput(
        cost_of_equity=10,
        cost_of_debt=5,
        tax_rate=0.25,
        equity_value=80,
        debt_value=20,
    )
    result = wacc(data)
    assert result.wacc == pytest.approx(8.75)


def test_capm() -> None:
    data = CapmInput(risk_free_rate=3, beta=1.2, market_return=8)
    result = capm(data)
    assert result.cost_of_equity == pytest.approx(9.0)


def test_npv() -> None:
    data = NpvInput(discount_rate=10, cash_flows=[-1000, 400, 400, 400])
    result = npv(data)
    assert result.npv == pytest.approx(-1000 + 400 / 1.1 + 400 / 1.1**2 + 400 / 1.1**3)


def test_irr_simple() -> None:
    data = IrrInput(cash_flows=[-1000, 1100])
    result = irr(data)
    assert result.irr == pytest.approx(10.0, rel=1e-2)


def test_dcf_terminal_growth() -> None:
    data = DcfInput(discount_rate=10, cash_flows=[100, 110, 121], terminal_growth=0.02)
    result = dcf(data)
    assert result.total_value > 0


def test_comps() -> None:
    data = CompsInput(metric=10, multiples=[5, 7, 9])
    result = comps(data)
    assert result.low == 50
    assert result.high == 90
    assert result.median == 70
