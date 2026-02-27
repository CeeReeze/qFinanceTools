from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from qfinancetools.models.explain import ExplanationBlock, WarningItem


class ScenarioInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    base_value: float = Field(..., ge=0)
    shocks: list[float] = Field(..., min_length=1)


class ScenarioResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    outcomes: list[float]
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None


class SensitivityInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    base_value: float = Field(..., ge=0)
    change: float = Field(...)


class SensitivityResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    new_value: float
    percent_change: float
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None


class MonteCarloInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    initial_value: float = Field(..., ge=0)
    mean_return: float = Field(...)
    volatility: float = Field(..., ge=0)
    years: int = Field(..., gt=0)
    simulations: int = Field(..., gt=0)
    seed: int = Field(0, ge=0)


class MonteCarloResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    mean: float
    median: float
    p5: float
    p95: float
    values: list[float]
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None


class StressTestInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    base_value: float = Field(..., ge=0)
    drawdown: float = Field(..., ge=0, le=1)


class StressTestResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    stressed_value: float
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None
