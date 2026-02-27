from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from qfinancetools.models.explain import ExplanationBlock, WarningItem

class WaccInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    cost_of_equity: float = Field(..., ge=0)
    cost_of_debt: float = Field(..., ge=0)
    tax_rate: float = Field(..., ge=0, le=1)
    equity_value: float = Field(..., ge=0)
    debt_value: float = Field(..., ge=0)


class WaccResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    wacc: float
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None


class CapmInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    risk_free_rate: float = Field(..., ge=0)
    beta: float
    market_return: float = Field(..., ge=0)


class CapmResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    cost_of_equity: float
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None


class NpvInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    discount_rate: float = Field(..., ge=0)
    cash_flows: list[float] = Field(..., min_length=1)


class NpvResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    npv: float
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None


class IrrInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    cash_flows: list[float] = Field(..., min_length=2)
    guess: float = Field(0.1, ge=-0.99)


class IrrResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    irr: float
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None


class DcfInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    discount_rate: float = Field(..., ge=0)
    cash_flows: list[float] = Field(..., min_length=1)
    terminal_growth: float = Field(0.0, ge=-0.99)
    terminal_multiple: float | None = None


class DcfResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    present_value: float
    terminal_value: float
    total_value: float
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None


class CompsInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    metric: float = Field(..., ge=0)
    multiples: list[float] = Field(..., min_length=1)


class CompsResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    low: float
    high: float
    median: float
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None
