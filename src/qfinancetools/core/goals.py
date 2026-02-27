from __future__ import annotations

from qfinancetools.core.explainability import investment_explanation, loan_explanation
from qfinancetools.core.guardrails import invest_warnings, loan_warnings
from qfinancetools.core.investments import investment_growth
from qfinancetools.core.loans import compute_monthly_payment, loan_summary
from qfinancetools.models.goals import (
    InvestmentGoalInput,
    InvestmentGoalResult,
    LoanPayoffGoalInput,
    LoanPayoffGoalResult,
)
from qfinancetools.models.investments import InvestmentInput
from qfinancetools.models.loans import LoanInput


def solve_investment_goal(data: InvestmentGoalInput) -> InvestmentGoalResult:
    if data.monthly is None and data.annual_rate is None:
        raise ValueError("Either monthly or annual_rate must be provided.")
    if data.monthly is not None and data.annual_rate is not None:
        raise ValueError("Provide only one unknown: monthly or annual_rate.")

    if data.annual_rate is not None:
        monthly_rate = data.annual_rate / 100 / 12
        months = data.years * 12
        if monthly_rate == 0:
            required_monthly = (data.target_value - data.initial) / months
        else:
            factor = (1 + monthly_rate) ** months
            annuity_factor = (factor - 1) / monthly_rate
            required_monthly = (data.target_value - data.initial * factor) / annuity_factor
        if required_monthly < 0:
            required_monthly = 0.0
        warnings = invest_warnings(data.initial, required_monthly, data.annual_rate, data.years)
        explanation = investment_explanation(
            data.initial, required_monthly, data.annual_rate, data.years, data.target_value
        )
        return InvestmentGoalResult(
            target_value=data.target_value,
            years=data.years,
            required_monthly=required_monthly,
            warnings=warnings,
            explanation=explanation,
        )

    low, high = 0.0, 100.0
    required_rate = None
    for _ in range(80):
        mid = (low + high) / 2
        result = investment_growth(
            InvestmentInput(
                initial=data.initial,
                monthly=data.monthly or 0.0,
                annual_rate=mid,
                years=data.years,
            )
        )
        if abs(result.final_value - data.target_value) < 1e-6:
            required_rate = mid
            break
        if result.final_value < data.target_value:
            low = mid
        else:
            high = mid
    if required_rate is None:
        required_rate = (low + high) / 2
    warnings = invest_warnings(data.initial, data.monthly or 0.0, required_rate, data.years)
    explanation = investment_explanation(data.initial, data.monthly or 0.0, required_rate, data.years, data.target_value)
    return InvestmentGoalResult(
        target_value=data.target_value,
        years=data.years,
        required_annual_rate=required_rate,
        warnings=warnings,
        explanation=explanation,
    )


def solve_loan_payoff_goal(data: LoanPayoffGoalInput) -> LoanPayoffGoalResult:
    if data.target_years > data.current_years:
        raise ValueError("target_years must be less than or equal to current_years")

    base_input = LoanInput(
        principal=data.principal,
        annual_rate=data.annual_rate,
        years=data.current_years,
        extra_payment=0.0,
    )
    base_payment = compute_monthly_payment(base_input)

    low = 0.0
    high = max(1.0, data.principal / (data.target_years * 12))
    for _ in range(50):
        test_input = LoanInput(
            principal=data.principal,
            annual_rate=data.annual_rate,
            years=data.current_years,
            extra_payment=high,
        )
        test_years = loan_summary(test_input).years
        if test_years <= data.target_years:
            break
        high *= 1.5

    for _ in range(80):
        mid = (low + high) / 2
        test_input = LoanInput(
            principal=data.principal,
            annual_rate=data.annual_rate,
            years=data.current_years,
            extra_payment=mid,
        )
        years = loan_summary(test_input).years
        if abs(years - data.target_years) < 1e-4:
            low = high = mid
            break
        if years > data.target_years:
            low = mid
        else:
            high = mid

    required_extra = (low + high) / 2
    warnings = loan_warnings(data.principal, data.annual_rate, data.current_years, required_extra)
    explanation = loan_explanation(data.principal, data.annual_rate, data.current_years, base_payment)
    return LoanPayoffGoalResult(
        base_monthly_payment=base_payment,
        required_extra_payment=required_extra,
        target_years=data.target_years,
        warnings=warnings,
        explanation=explanation,
    )
