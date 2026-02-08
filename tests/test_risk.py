import pytest

from qbanker.core.risk import scenario, sensitivity, monte_carlo, stress_test
from qbanker.models.risk import ScenarioInput, SensitivityInput, MonteCarloInput, StressTestInput


def test_scenario() -> None:
    data = ScenarioInput(base_value=100, shocks=[-10, 0, 10])
    result = scenario(data)
    assert result.outcomes == pytest.approx([90, 100, 110])


def test_sensitivity() -> None:
    data = SensitivityInput(base_value=100, change=5)
    result = sensitivity(data)
    assert result.new_value == 105


def test_monte_carlo_deterministic() -> None:
    data = MonteCarloInput(
        initial_value=100,
        mean_return=5,
        volatility=0,
        years=2,
        simulations=3,
        seed=42,
    )
    result = monte_carlo(data)
    assert result.mean == 110.25
    assert result.p5 == 110.25
    assert result.p95 == 110.25


def test_stress_test() -> None:
    data = StressTestInput(base_value=1000, drawdown=0.2)
    result = stress_test(data)
    assert result.stressed_value == 800
