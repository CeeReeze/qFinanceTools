from qfinancetools.core.timeline import build_unified_timeline
from qfinancetools.models.bonds import BondPriceInput
from qfinancetools.models.investments import InvestmentInput
from qfinancetools.models.loans import LoanInput
from qfinancetools.models.stocks import StockProjectionInput
from qfinancetools.models.timeline import TimelineRequest


def test_timeline_basic() -> None:
    result = build_unified_timeline(
        TimelineRequest(months=24),
        loan_input=LoanInput(principal=100000, annual_rate=5, years=30, extra_payment=0),
        invest_input=InvestmentInput(initial=1000, monthly=100, annual_rate=7, years=2),
        bond_input=BondPriceInput(face_value=1000, coupon_rate=5, yield_rate=4.5, years=2, payments_per_year=2),
        stock_input=StockProjectionInput(
            ticker="SPY",
            initial=1000,
            monthly=100,
            annual_return=8,
            years=2,
            expense_ratio=0.03,
        ),
    )
    assert result.months == 24
    assert len(result.series) == 4
    assert len(result.net) == 24
