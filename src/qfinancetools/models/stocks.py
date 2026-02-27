from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from qfinancetools.models.explain import ExplanationBlock, WarningItem


class StockProjectionInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    ticker: str = Field(..., min_length=1)
    initial: float = Field(..., ge=0)
    monthly: float = Field(0, ge=0)
    annual_return: float = Field(..., ge=0)
    years: int = Field(..., gt=0)
    expense_ratio: float = Field(0.0, ge=0)


class StockProjectionResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    ticker: str
    final_value: float
    total_contributions: float
    total_growth: float
    effective_annual_return: float
    warnings: list[WarningItem] = Field(default_factory=list)
    explanation: ExplanationBlock | None = None


class StockHistoryInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    tickers: list[str] = Field(..., min_length=1)
    start_date: str | None = None
    end_date: str | None = None
    period_years: int = Field(5, gt=0)
    weights: list[float] | None = None


class StockHistoryPoint(BaseModel):
    model_config = ConfigDict(frozen=True)

    date: str
    price: float | None = None
    normalized: float


class StockHistorySeries(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    points: list[StockHistoryPoint] = Field(default_factory=list)
    last_updated: str
    stale: bool


class StockHistoryResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    source: str
    start_date: str
    end_date: str
    series: list[StockHistorySeries] = Field(default_factory=list)
    warnings: list[WarningItem] = Field(default_factory=list)


class StockBacktestInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    tickers: list[str] = Field(..., min_length=1)
    start_date: str | None = None
    end_date: str | None = None
    period_years: int = Field(5, gt=0)
    lump_sum: float = Field(0.0, ge=0)
    periodic_amount: float = Field(0.0, ge=0)
    periodic_months: int = Field(1, gt=0)
    weights: list[float] | None = None


class StockBacktestPoint(BaseModel):
    model_config = ConfigDict(frozen=True)

    date: str
    invested: float
    value: float
    revenue: float


class StockBacktestResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    source: str
    start_date: str
    end_date: str
    final_invested: float
    final_value: float
    final_revenue: float
    final_return_percent: float
    timeline: list[StockBacktestPoint] = Field(default_factory=list)
    last_updated: str
    stale: bool
    warnings: list[WarningItem] = Field(default_factory=list)
