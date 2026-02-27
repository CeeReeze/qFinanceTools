from __future__ import annotations

from qfinancetools.core.investments import investment_growth
from qfinancetools.core.loans import loan_summary
from qfinancetools.core.risk import monte_carlo
from qfinancetools.models.comparison import ComparisonDelta, ComparisonRequest, ComparisonResult
from qfinancetools.models.investments import InvestmentInput
from qfinancetools.models.loans import LoanInput
from qfinancetools.models.risk import MonteCarloInput


def _build_delta(metric: str, base_value: float, alt_value: float) -> ComparisonDelta:
    absolute_delta = alt_value - base_value
    if base_value == 0:
        return ComparisonDelta(
            metric=metric,
            base_value=base_value,
            alt_value=alt_value,
            absolute_delta=absolute_delta,
            percent_delta=None,
            percent_delta_reason="base_value is zero",
        )
    return ComparisonDelta(
        metric=metric,
        base_value=base_value,
        alt_value=alt_value,
        absolute_delta=absolute_delta,
        percent_delta=(absolute_delta / base_value) * 100,
    )


def _loan_comparison(request: ComparisonRequest) -> ComparisonResult:
    base_input = LoanInput(
        principal=float(request.base.inputs["amount"]),
        annual_rate=float(request.base.inputs["rate"]),
        years=int(request.base.inputs["years"]),
        extra_payment=float(request.base.inputs.get("extra", 0.0)),
    )
    alt_input = LoanInput(
        principal=float(request.alt.inputs["amount"]),
        annual_rate=float(request.alt.inputs["rate"]),
        years=int(request.alt.inputs["years"]),
        extra_payment=float(request.alt.inputs.get("extra", 0.0)),
    )
    base = loan_summary(base_input)
    alt = loan_summary(alt_input)
    return ComparisonResult(
        calculator="loan",
        base_label=request.base.label,
        alt_label=request.alt.label,
        deltas=[
            _build_delta("monthly_payment", base.monthly_payment, alt.monthly_payment),
            _build_delta("total_interest", base.total_interest, alt.total_interest),
            _build_delta("total_paid", base.total_paid, alt.total_paid),
            _build_delta("years", base.years, alt.years),
        ],
    )


def _invest_comparison(request: ComparisonRequest) -> ComparisonResult:
    base_input = InvestmentInput(
        initial=float(request.base.inputs["initial"]),
        monthly=float(request.base.inputs["monthly"]),
        annual_rate=float(request.base.inputs["rate"]),
        years=int(request.base.inputs["years"]),
    )
    alt_input = InvestmentInput(
        initial=float(request.alt.inputs["initial"]),
        monthly=float(request.alt.inputs["monthly"]),
        annual_rate=float(request.alt.inputs["rate"]),
        years=int(request.alt.inputs["years"]),
    )
    base = investment_growth(base_input)
    alt = investment_growth(alt_input)
    return ComparisonResult(
        calculator="invest",
        base_label=request.base.label,
        alt_label=request.alt.label,
        deltas=[
            _build_delta("final_value", base.final_value, alt.final_value),
            _build_delta("total_contributions", base.total_contributions, alt.total_contributions),
            _build_delta("total_growth", base.total_growth, alt.total_growth),
        ],
    )


def _risk_comparison(request: ComparisonRequest) -> ComparisonResult:
    base_input = MonteCarloInput(
        initial_value=float(request.base.inputs["initial"]),
        mean_return=float(request.base.inputs["mean"]),
        volatility=float(request.base.inputs["volatility"]),
        years=int(request.base.inputs["years"]),
        simulations=int(request.base.inputs["sims"]),
        seed=int(request.base.inputs.get("seed", 42)),
    )
    alt_input = MonteCarloInput(
        initial_value=float(request.alt.inputs["initial"]),
        mean_return=float(request.alt.inputs["mean"]),
        volatility=float(request.alt.inputs["volatility"]),
        years=int(request.alt.inputs["years"]),
        simulations=int(request.alt.inputs["sims"]),
        seed=int(request.alt.inputs.get("seed", 42)),
    )
    base = monte_carlo(base_input)
    alt = monte_carlo(alt_input)
    return ComparisonResult(
        calculator="risk",
        base_label=request.base.label,
        alt_label=request.alt.label,
        deltas=[
            _build_delta("mean", base.mean, alt.mean),
            _build_delta("median", base.median, alt.median),
            _build_delta("p5", base.p5, alt.p5),
            _build_delta("p95", base.p95, alt.p95),
        ],
    )


def compare_scenarios(request: ComparisonRequest) -> ComparisonResult:
    calculator = request.calculator.lower().strip()
    if calculator == "loan":
        return _loan_comparison(request)
    if calculator == "invest":
        return _invest_comparison(request)
    if calculator == "risk":
        return _risk_comparison(request)
    raise ValueError(f"Unsupported comparison calculator: {request.calculator}")
