from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class WarningItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    message: str
    severity: str = Field(default="warning")


class FormulaStep(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    formula: str
    value: float | str


class ExplanationBlock(BaseModel):
    model_config = ConfigDict(frozen=True)

    summary: str
    steps: list[FormulaStep] = Field(default_factory=list)
