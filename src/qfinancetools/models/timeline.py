from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from qfinancetools.models.explain import WarningItem


class TimelineRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    months: int = Field(..., gt=0)
    include_loan: bool = True
    include_invest: bool = True
    include_bonds: bool = True
    include_stocks: bool = True


class TimelinePoint(BaseModel):
    model_config = ConfigDict(frozen=True)

    month: int
    amount: float
    running_total: float


class TimelineSeries(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    points: list[TimelinePoint] = Field(default_factory=list)


class TimelineResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    months: int
    series: list[TimelineSeries] = Field(default_factory=list)
    net: list[TimelinePoint] = Field(default_factory=list)
    warnings: list[WarningItem] = Field(default_factory=list)
