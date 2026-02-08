import pytest

from qbanker.core.investments import investment_growth
from qbanker.models.investments import InvestmentInput


def test_investment_zero_rate() -> None:
    data = InvestmentInput(initial=10000, monthly=0, annual_rate=0, years=2)
    result = investment_growth(data)
    assert result.final_value == 10000
    assert result.total_growth == 0


def test_investment_growth_known_formula() -> None:
    data = InvestmentInput(initial=1000, monthly=100, annual_rate=12, years=1)
    result = investment_growth(data)

    r = 0.12 / 12
    n = 12
    factor = (1 + r) ** n
    expected = 1000 * factor + 100 * ((factor - 1) / r)
    assert result.final_value == pytest.approx(expected, rel=1e-9)
