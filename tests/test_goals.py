from qfinancetools.core.goals import solve_investment_goal, solve_loan_payoff_goal
from qfinancetools.models.goals import InvestmentGoalInput, LoanPayoffGoalInput


def test_investment_goal_solve_monthly() -> None:
    result = solve_investment_goal(
        InvestmentGoalInput(
            target_value=500000,
            initial=50000,
            years=20,
            annual_rate=7,
        )
    )
    assert result.required_monthly is not None
    assert result.required_monthly >= 0


def test_investment_goal_solve_rate() -> None:
    result = solve_investment_goal(
        InvestmentGoalInput(
            target_value=500000,
            initial=50000,
            years=20,
            monthly=500,
        )
    )
    assert result.required_annual_rate is not None
    assert result.required_annual_rate >= 0


def test_loan_payoff_goal() -> None:
    result = solve_loan_payoff_goal(
        LoanPayoffGoalInput(
            principal=350000,
            annual_rate=5.4,
            current_years=25,
            target_years=20,
        )
    )
    assert result.required_extra_payment > 0
