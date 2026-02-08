import pytest

from qbanker.core.loans import compute_monthly_payment, loan_summary
from qbanker.models.loans import LoanInput


def test_monthly_payment_zero_rate() -> None:
    data = LoanInput(principal=12000, annual_rate=0, years=1, extra_payment=0)
    payment = compute_monthly_payment(data)
    assert payment == 1000


def test_monthly_payment_known_value() -> None:
    data = LoanInput(principal=100000, annual_rate=6, years=30, extra_payment=0)
    payment = compute_monthly_payment(data)
    assert payment == pytest.approx(599.55, rel=1e-3)


def test_loan_summary_totals() -> None:
    data = LoanInput(principal=10000, annual_rate=5, years=2, extra_payment=0)
    result = loan_summary(data)
    assert result.total_paid >= data.principal
    assert result.total_interest >= 0
