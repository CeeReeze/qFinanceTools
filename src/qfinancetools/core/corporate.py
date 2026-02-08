from __future__ import annotations

import math

from qfinancetools.models.corporate import (
    WaccInput,
    WaccResult,
    CapmInput,
    CapmResult,
    NpvInput,
    NpvResult,
    IrrInput,
    IrrResult,
    DcfInput,
    DcfResult,
    CompsInput,
    CompsResult,
)


def wacc(data: WaccInput) -> WaccResult:
    total = data.equity_value + data.debt_value
    if total == 0:
        raise ValueError("equity_value + debt_value must be positive")
    equity_weight = data.equity_value / total
    debt_weight = data.debt_value / total
    wacc_value = equity_weight * data.cost_of_equity + debt_weight * data.cost_of_debt * (1 - data.tax_rate)
    return WaccResult(wacc=wacc_value)


def capm(data: CapmInput) -> CapmResult:
    cost = data.risk_free_rate + data.beta * (data.market_return - data.risk_free_rate)
    return CapmResult(cost_of_equity=cost)


def npv(data: NpvInput) -> NpvResult:
    rate = data.discount_rate / 100
    value = 0.0
    for idx, cash in enumerate(data.cash_flows):
        value += cash / ((1 + rate) ** idx)
    return NpvResult(npv=value)


def _npv_for_rate(cash_flows: list[float], rate: float) -> float:
    value = 0.0
    for idx, cash in enumerate(cash_flows):
        value += cash / ((1 + rate) ** idx)
    return value


def irr(data: IrrInput) -> IrrResult:
    cash_flows = data.cash_flows
    rate = data.guess
    for _ in range(100):
        f = _npv_for_rate(cash_flows, rate)
        derivative = 0.0
        for idx, cash in enumerate(cash_flows[1:], start=1):
            derivative -= idx * cash / ((1 + rate) ** (idx + 1))
        if derivative == 0:
            break
        next_rate = rate - f / derivative
        if abs(next_rate - rate) < 1e-10:
            return IrrResult(irr=next_rate * 100)
        rate = next_rate

    low, high = -0.99, 10.0
    for _ in range(200):
        mid = (low + high) / 2
        value = _npv_for_rate(cash_flows, mid)
        if abs(value) < 1e-8:
            return IrrResult(irr=mid * 100)
        if value > 0:
            low = mid
        else:
            high = mid
    return IrrResult(irr=rate * 100)


def dcf(data: DcfInput) -> DcfResult:
    rate = data.discount_rate / 100
    pv = 0.0
    for idx, cash in enumerate(data.cash_flows, start=1):
        pv += cash / ((1 + rate) ** idx)

    terminal_value = 0.0
    if data.terminal_multiple is not None:
        terminal_value = data.cash_flows[-1] * data.terminal_multiple
    else:
        if rate <= data.terminal_growth:
            raise ValueError("discount_rate must exceed terminal_growth")
        terminal_value = data.cash_flows[-1] * (1 + data.terminal_growth) / (rate - data.terminal_growth)

    pv_terminal = terminal_value / ((1 + rate) ** len(data.cash_flows))
    total_value = pv + pv_terminal

    return DcfResult(present_value=pv, terminal_value=terminal_value, total_value=total_value)


def comps(data: CompsInput) -> CompsResult:
    multiples = sorted(data.multiples)
    low = multiples[0] * data.metric
    high = multiples[-1] * data.metric
    mid = multiples[len(multiples) // 2]
    median = mid * data.metric
    return CompsResult(low=low, high=high, median=median)
