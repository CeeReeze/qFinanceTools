from qfinancetools.core.loans import compute_monthly_payment, amortization_schedule, loan_summary
from qfinancetools.core.investments import investment_growth
from qfinancetools.core.afford import affordability
from qfinancetools.core.corporate import wacc, capm, npv, irr, dcf, comps
from qfinancetools.core.bonds import (
    bond_price,
    bond_ytm,
    bond_duration,
    bond_convexity,
    bond_ladder,
)
from qfinancetools.core.risk import scenario, sensitivity, monte_carlo, stress_test
from qfinancetools.core.comparison import compare_scenarios
from qfinancetools.core.timeline import build_unified_timeline
from qfinancetools.core.goals import solve_investment_goal, solve_loan_payoff_goal
from qfinancetools.core.plugins import discover_plugins
from qfinancetools.core.stocks import stock_projection, stock_history, stock_backtest

__all__ = [
    "compute_monthly_payment",
    "amortization_schedule",
    "loan_summary",
    "investment_growth",
    "affordability",
    "wacc",
    "capm",
    "npv",
    "irr",
    "dcf",
    "comps",
    "bond_price",
    "bond_ytm",
    "bond_duration",
    "bond_convexity",
    "bond_ladder",
    "scenario",
    "sensitivity",
    "monte_carlo",
    "stress_test",
    "compare_scenarios",
    "build_unified_timeline",
    "solve_investment_goal",
    "solve_loan_payoff_goal",
    "discover_plugins",
    "stock_projection",
    "stock_history",
    "stock_backtest",
]
