from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class BondPriceInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    face_value: float = Field(..., gt=0)
    coupon_rate: float = Field(..., ge=0)
    yield_rate: float = Field(..., ge=0)
    years: int = Field(..., gt=0)
    payments_per_year: int = Field(2, gt=0)


class BondPriceResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    price: float


class BondYtmInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    face_value: float = Field(..., gt=0)
    coupon_rate: float = Field(..., ge=0)
    price: float = Field(..., gt=0)
    years: int = Field(..., gt=0)
    payments_per_year: int = Field(2, gt=0)
    guess: float = Field(0.05, ge=0)


class BondYtmResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    yield_rate: float


class BondDurationInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    face_value: float = Field(..., gt=0)
    coupon_rate: float = Field(..., ge=0)
    yield_rate: float = Field(..., ge=0)
    years: int = Field(..., gt=0)
    payments_per_year: int = Field(2, gt=0)


class BondDurationResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    macaulay_duration: float
    modified_duration: float


class BondConvexityInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    face_value: float = Field(..., gt=0)
    coupon_rate: float = Field(..., ge=0)
    yield_rate: float = Field(..., ge=0)
    years: int = Field(..., gt=0)
    payments_per_year: int = Field(2, gt=0)


class BondConvexityResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    convexity: float


class BondLadderInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    maturities: list[int] = Field(..., min_length=1)
    amounts: list[float] = Field(..., min_length=1)


class BondLadderResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    total_invested: float
    weighted_maturity: float
    schedule: list[tuple[int, float]]
