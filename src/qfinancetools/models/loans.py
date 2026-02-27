from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from qfinancetools.models.explain import ExplanationBlock, WarningItem


class LoanInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    principal: float = Field(..., gt=0)
    annual_rate: float = Field(..., ge=0)
    years: int = Field(..., gt=0)
    extra_payment: float = Field(0, ge=0)


class LoanResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    monthly_payment: float
    total_interest: float
    total_paid: float
    years: float
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None


class AmortizationRow(BaseModel):
    model_config = ConfigDict(frozen=True)

    month: int
    payment: float
    principal: float
    interest: float
    balance: float

    @field_validator("month")
    @classmethod
    def _positive_month(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("month must be positive")
        return value
