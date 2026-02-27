from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from qfinancetools.models.explain import ExplanationBlock, WarningItem


class AffordInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    income_monthly: float = Field(..., gt=0)
    debts_monthly: float = Field(..., ge=0)
    housing_cost: float = Field(..., ge=0)
    max_dti: float = Field(..., gt=0, le=1)
    stress_rate: float = Field(..., ge=0)


class AffordResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    allowed_housing: float
    current_dti: float
    stressed_dti: float
    affordable: bool
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None
