from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class InvestmentInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    initial: float = Field(..., ge=0)
    monthly: float = Field(..., ge=0)
    annual_rate: float = Field(..., ge=0)
    years: int = Field(..., gt=0)


class InvestmentResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    final_value: float
    total_contributions: float
    total_growth: float
    years: float
