from __future__ import annotations

import random

from qfinancetools.models.risk import (
    ScenarioInput,
    ScenarioResult,
    SensitivityInput,
    SensitivityResult,
    MonteCarloInput,
    MonteCarloResult,
    StressTestInput,
    StressTestResult,
)


def scenario(data: ScenarioInput) -> ScenarioResult:
    outcomes = [data.base_value * (1 + shock / 100) for shock in data.shocks]
    return ScenarioResult(outcomes=outcomes)


def sensitivity(data: SensitivityInput) -> SensitivityResult:
    new_value = data.base_value * (1 + data.change / 100)
    percent_change = (new_value - data.base_value) / data.base_value if data.base_value else 0.0
    return SensitivityResult(new_value=new_value, percent_change=percent_change)


def monte_carlo(data: MonteCarloInput) -> MonteCarloResult:
    rng = random.Random(data.seed)
    steps = data.years
    values: list[float] = []

    for _ in range(data.simulations):
        value = data.initial_value
        for _ in range(steps):
            draw = rng.gauss(data.mean_return, data.volatility)
            value *= 1 + draw / 100
        values.append(value)

    values.sort()
    mean = sum(values) / len(values)
    mid = len(values) // 2
    if len(values) % 2 == 0:
        median = (values[mid - 1] + values[mid]) / 2
    else:
        median = values[mid]

    p5 = values[int(0.05 * (len(values) - 1))]
    p95 = values[int(0.95 * (len(values) - 1))]

    return MonteCarloResult(mean=mean, median=median, p5=p5, p95=p95)


def stress_test(data: StressTestInput) -> StressTestResult:
    stressed = data.base_value * (1 - data.drawdown)
    return StressTestResult(stressed_value=stressed)
