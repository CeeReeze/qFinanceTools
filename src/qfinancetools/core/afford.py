from __future__ import annotations

from qfinancetools.models.afford import AffordInput, AffordResult


def affordability(data: AffordInput) -> AffordResult:
    income = data.income_monthly
    if income <= 0:
        raise ValueError("income_monthly must be positive")

    current_dti = (data.debts_monthly + data.housing_cost) / income
    stressed_housing = data.housing_cost * (1 + data.stress_rate / 100)
    stressed_dti = (data.debts_monthly + stressed_housing) / income
    allowed_housing = income * data.max_dti - data.debts_monthly
    if allowed_housing < 0:
        allowed_housing = 0

    affordable = current_dti <= data.max_dti and stressed_dti <= data.max_dti

    return AffordResult(
        allowed_housing=allowed_housing,
        current_dti=current_dti,
        stressed_dti=stressed_dti,
        affordable=affordable,
    )
