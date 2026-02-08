import pytest

from qfinancetools.core.bonds import bond_price, bond_ytm, bond_duration, bond_convexity, bond_ladder
from qfinancetools.models.bonds import (
    BondPriceInput,
    BondYtmInput,
    BondDurationInput,
    BondConvexityInput,
    BondLadderInput,
)


def test_bond_price_zero_coupon() -> None:
    data = BondPriceInput(face_value=1000, coupon_rate=0, yield_rate=5, years=2, payments_per_year=1)
    result = bond_price(data)
    expected = 1000 / (1.05**2)
    assert result.price == pytest.approx(expected)


def test_bond_ytm_roundtrip() -> None:
    price_data = BondPriceInput(face_value=1000, coupon_rate=5, yield_rate=4, years=5, payments_per_year=2)
    price = bond_price(price_data).price
    ytm_data = BondYtmInput(face_value=1000, coupon_rate=5, price=price, years=5, payments_per_year=2)
    ytm = bond_ytm(ytm_data).yield_rate
    assert ytm == pytest.approx(4.0, rel=1e-3)


def test_bond_duration_convexity() -> None:
    duration_data = BondDurationInput(face_value=1000, coupon_rate=5, yield_rate=5, years=10, payments_per_year=2)
    convexity_data = BondConvexityInput(face_value=1000, coupon_rate=5, yield_rate=5, years=10, payments_per_year=2)
    duration = bond_duration(duration_data)
    convexity = bond_convexity(convexity_data)
    assert duration.macaulay_duration > 0
    assert convexity.convexity > 0


def test_bond_ladder() -> None:
    data = BondLadderInput(maturities=[1, 3, 5], amounts=[1000, 1000, 2000])
    result = bond_ladder(data)
    assert result.total_invested == 4000
    assert result.weighted_maturity == pytest.approx((1*1000 + 3*1000 + 5*2000) / 4000)
