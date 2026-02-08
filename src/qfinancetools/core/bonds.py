from __future__ import annotations

from qfinancetools.models.bonds import (
    BondPriceInput,
    BondPriceResult,
    BondYtmInput,
    BondYtmResult,
    BondDurationInput,
    BondDurationResult,
    BondConvexityInput,
    BondConvexityResult,
    BondLadderInput,
    BondLadderResult,
)


def bond_price(data: BondPriceInput) -> BondPriceResult:
    periods = data.years * data.payments_per_year
    rate = data.yield_rate / 100 / data.payments_per_year
    coupon = data.face_value * data.coupon_rate / 100 / data.payments_per_year

    price = 0.0
    for t in range(1, periods + 1):
        price += coupon / ((1 + rate) ** t)
    price += data.face_value / ((1 + rate) ** periods)

    return BondPriceResult(price=price)


def bond_ytm(data: BondYtmInput) -> BondYtmResult:
    periods = data.years * data.payments_per_year
    coupon = data.face_value * data.coupon_rate / 100 / data.payments_per_year

    low, high = 0.0, 1.0
    for _ in range(100):
        mid = (low + high) / 2
        price = 0.0
        for t in range(1, periods + 1):
            price += coupon / ((1 + mid) ** t)
        price += data.face_value / ((1 + mid) ** periods)
        if abs(price - data.price) < 1e-8:
            return BondYtmResult(yield_rate=mid * data.payments_per_year * 100)
        if price > data.price:
            low = mid
        else:
            high = mid

    return BondYtmResult(yield_rate=mid * data.payments_per_year * 100)


def bond_duration(data: BondDurationInput) -> BondDurationResult:
    periods = data.years * data.payments_per_year
    rate = data.yield_rate / 100 / data.payments_per_year
    coupon = data.face_value * data.coupon_rate / 100 / data.payments_per_year

    pv_total = 0.0
    weighted_sum = 0.0
    for t in range(1, periods + 1):
        cash = coupon
        if t == periods:
            cash += data.face_value
        pv = cash / ((1 + rate) ** t)
        pv_total += pv
        weighted_sum += t * pv

    macaulay = weighted_sum / pv_total / data.payments_per_year
    modified = macaulay / (1 + data.yield_rate / 100 / data.payments_per_year)

    return BondDurationResult(macaulay_duration=macaulay, modified_duration=modified)


def bond_convexity(data: BondConvexityInput) -> BondConvexityResult:
    periods = data.years * data.payments_per_year
    rate = data.yield_rate / 100 / data.payments_per_year
    coupon = data.face_value * data.coupon_rate / 100 / data.payments_per_year

    pv_total = 0.0
    convex_sum = 0.0
    for t in range(1, periods + 1):
        cash = coupon
        if t == periods:
            cash += data.face_value
        discount = (1 + rate) ** t
        pv = cash / discount
        pv_total += pv
        convex_sum += t * (t + 1) * cash / (discount * (1 + rate) ** 0)

    convexity = convex_sum / (pv_total * (1 + rate) ** 2) / (data.payments_per_year**2)

    return BondConvexityResult(convexity=convexity)


def bond_ladder(data: BondLadderInput) -> BondLadderResult:
    if len(data.maturities) != len(data.amounts):
        raise ValueError("maturities and amounts must have the same length")

    total = sum(data.amounts)
    if total <= 0:
        raise ValueError("total invested must be positive")

    weighted = 0.0
    schedule: list[tuple[int, float]] = []
    for maturity, amount in sorted(zip(data.maturities, data.amounts), key=lambda x: x[0]):
        weighted += maturity * amount
        schedule.append((maturity, amount))

    return BondLadderResult(
        total_invested=total,
        weighted_maturity=weighted / total,
        schedule=schedule,
    )
