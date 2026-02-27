from __future__ import annotations

from qfinancetools.models.investments import InvestmentInput, InvestmentResult
from qfinancetools.core.explainability import investment_explanation
from qfinancetools.core.guardrails import invest_warnings


def investment_growth(data: InvestmentInput) -> InvestmentResult:
    months = data.years * 12
    if months <= 0:
        raise ValueError("years must be positive")

    monthly_rate = data.annual_rate / 100 / 12
    if monthly_rate == 0:
        final_value = data.initial + data.monthly * months
    else:
        factor = (1 + monthly_rate) ** months
        annuity_factor = (factor - 1) / monthly_rate
        final_value = data.initial * factor + data.monthly * annuity_factor

    total_contributions = data.initial + data.monthly * months
    total_growth = final_value - total_contributions
    warnings = invest_warnings(data.initial, data.monthly, data.annual_rate, data.years)
    explanation = investment_explanation(data.initial, data.monthly, data.annual_rate, data.years, final_value)

    return InvestmentResult(
        final_value=final_value,
        total_contributions=total_contributions,
        total_growth=total_growth,
        years=float(data.years),
        warnings=warnings,
        explanation=explanation,
    )
