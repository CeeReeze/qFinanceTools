from __future__ import annotations

from qfinancetools.models.investments import InvestmentInput, InvestmentResult


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

    return InvestmentResult(
        final_value=final_value,
        total_contributions=total_contributions,
        total_growth=total_growth,
        years=float(data.years),
    )
