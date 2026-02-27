from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from qfinancetools.models.explain import ExplanationBlock, WarningItem


class InvestmentGoalInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    target_value: float = Field(..., gt=0)
    initial: float = Field(..., ge=0)
    years: int = Field(..., gt=0)
    monthly: float | None = Field(default=None, ge=0)
    annual_rate: float | None = Field(default=None, ge=0)


class InvestmentGoalResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    target_value: float
    years: int
    required_monthly: float | None = None
    required_annual_rate: float | None = None
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None


class LoanPayoffGoalInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    principal: float = Field(..., gt=0)
    annual_rate: float = Field(..., ge=0)
    current_years: int = Field(..., gt=0)
    target_years: int = Field(..., gt=0)


class LoanPayoffGoalResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    base_monthly_payment: float
    required_extra_payment: float
    target_years: int
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None
