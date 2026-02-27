from __future__ import annotations

from qfinancetools.models.explain import WarningItem


def loan_warnings(principal: float, annual_rate: float, years: int, extra_payment: float) -> list[WarningItem]:
    warnings: list[WarningItem] = []
    if annual_rate > 20:
        warnings.append(WarningItem(code="loan.high_rate", message="Annual rate is unusually high (>20%)."))
    if years > 40:
        warnings.append(WarningItem(code="loan.long_term", message="Loan term is unusually long (>40 years)."))
    if extra_payment > principal * 0.1:
        warnings.append(WarningItem(code="loan.large_extra", message="Extra payment is unusually large relative to principal."))
    return warnings


def invest_warnings(initial: float, monthly: float, annual_rate: float, years: int) -> list[WarningItem]:
    warnings: list[WarningItem] = []
    if annual_rate > 25:
        warnings.append(WarningItem(code="invest.high_return", message="Assumed annual return is unusually high (>25%)."))
    if years > 60:
        warnings.append(WarningItem(code="invest.long_horizon", message="Investment horizon is unusually long (>60 years)."))
    if monthly == 0 and initial == 0:
        warnings.append(WarningItem(code="invest.no_contrib", message="No starting capital or monthly contribution was provided."))
    return warnings


def risk_warnings(mean_return: float | None = None, volatility: float | None = None, simulations: int | None = None) -> list[WarningItem]:
    warnings: list[WarningItem] = []
    if mean_return is not None and abs(mean_return) > 40:
        warnings.append(WarningItem(code="risk.extreme_mean", message="Mean return assumption is extreme (>|40|%)."))
    if volatility is not None and volatility > 80:
        warnings.append(WarningItem(code="risk.extreme_vol", message="Volatility assumption is unusually high (>80%)."))
    if simulations is not None and simulations < 500:
        warnings.append(WarningItem(code="risk.low_sims", message="Low simulation count may produce unstable Monte Carlo percentiles."))
    return warnings


def bonds_warnings(yield_rate: float | None = None, coupon_rate: float | None = None, years: int | None = None) -> list[WarningItem]:
    warnings: list[WarningItem] = []
    if yield_rate is not None and yield_rate > 20:
        warnings.append(WarningItem(code="bonds.high_yield", message="Yield input is unusually high (>20%)."))
    if coupon_rate is not None and coupon_rate > 20:
        warnings.append(WarningItem(code="bonds.high_coupon", message="Coupon input is unusually high (>20%)."))
    if years is not None and years > 50:
        warnings.append(WarningItem(code="bonds.long_maturity", message="Bond maturity is unusually long (>50 years)."))
    return warnings
