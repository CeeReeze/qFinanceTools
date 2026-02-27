from __future__ import annotations

from qfinancetools.models.explain import ExplanationBlock, FormulaStep


def loan_explanation(principal: float, annual_rate: float, years: int, monthly_payment: float) -> ExplanationBlock:
    return ExplanationBlock(
        summary="Monthly loan payment is computed from principal, annual rate, and term.",
        steps=[
            FormulaStep(name="Monthly rate", formula="r = annual_rate / 100 / 12", value=annual_rate / 100 / 12),
            FormulaStep(name="Periods", formula="n = years * 12", value=years * 12),
            FormulaStep(name="Payment", formula="P = L*r*(1+r)^n / ((1+r)^n - 1)", value=monthly_payment),
            FormulaStep(name="Principal", formula="L = principal", value=principal),
        ],
    )


def investment_explanation(initial: float, monthly: float, annual_rate: float, years: int, final_value: float) -> ExplanationBlock:
    return ExplanationBlock(
        summary="Future value combines compounded initial capital and monthly contribution annuity.",
        steps=[
            FormulaStep(name="Monthly rate", formula="r = annual_rate / 100 / 12", value=annual_rate / 100 / 12),
            FormulaStep(name="Periods", formula="n = years * 12", value=years * 12),
            FormulaStep(name="Initial growth", formula="initial * (1+r)^n", value=initial),
            FormulaStep(name="Result", formula="FV = initial growth + contribution growth", value=final_value),
            FormulaStep(name="Monthly contribution", formula="PMT = monthly", value=monthly),
        ],
    )


def monte_carlo_explanation(mean: float, median: float, p5: float, p95: float) -> ExplanationBlock:
    return ExplanationBlock(
        summary="Distribution statistics are computed from sorted simulation outcomes.",
        steps=[
            FormulaStep(name="Mean", formula="sum(values) / count(values)", value=mean),
            FormulaStep(name="Median", formula="middle(sorted(values))", value=median),
            FormulaStep(name="P5", formula="sorted(values)[floor(0.05*(n-1))]", value=p5),
            FormulaStep(name="P95", formula="sorted(values)[floor(0.95*(n-1))]", value=p95),
        ],
    )
