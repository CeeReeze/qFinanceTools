from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ComparisonCase(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    inputs: dict[str, float | int | str | list[float] | list[int]]


class ComparisonRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    calculator: str
    base: ComparisonCase
    alt: ComparisonCase


class ComparisonDelta(BaseModel):
    model_config = ConfigDict(frozen=True)

    metric: str
    base_value: float
    alt_value: float
    absolute_delta: float
    percent_delta: float | None = None
    percent_delta_reason: str | None = None


class ComparisonResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    calculator: str
    base_label: str
    alt_label: str
    deltas: list[ComparisonDelta] = Field(default_factory=list)
