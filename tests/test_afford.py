from qbanker.core.afford import affordability
from qbanker.models.afford import AffordInput


def test_affordability_thresholds() -> None:
    data = AffordInput(
        income_monthly=7000,
        debts_monthly=600,
        housing_cost=2200,
        max_dti=0.36,
        stress_rate=2,
    )
    result = affordability(data)
    assert result.current_dti == (600 + 2200) / 7000
    assert result.stressed_dti > result.current_dti
    assert result.affordable is False
