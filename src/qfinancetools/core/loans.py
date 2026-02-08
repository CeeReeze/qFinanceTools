from __future__ import annotations

from qfinancetools.models.loans import LoanInput, LoanResult, AmortizationRow


def compute_monthly_payment(loan: LoanInput) -> float:
    months = loan.years * 12
    if months <= 0:
        raise ValueError("years must be positive")
    monthly_rate = loan.annual_rate / 100 / 12
    if monthly_rate == 0:
        return loan.principal / months

    factor = (1 + monthly_rate) ** months
    return loan.principal * monthly_rate * factor / (factor - 1)


def amortization_schedule(loan: LoanInput) -> list[AmortizationRow]:
    monthly_rate = loan.annual_rate / 100 / 12
    base_payment = compute_monthly_payment(loan)
    balance = loan.principal
    schedule: list[AmortizationRow] = []
    month = 0
    max_months = loan.years * 12 * 2

    while balance > 1e-8:
        month += 1
        if month > max_months:
            raise ValueError("amortization exceeded maximum months; check inputs")

        interest = balance * monthly_rate
        total_payment = base_payment + loan.extra_payment
        principal_paid = total_payment - interest
        if principal_paid < 0:
            raise ValueError("payment does not cover interest")
        if principal_paid > balance:
            principal_paid = balance
            total_payment = interest + principal_paid

        balance = balance - principal_paid

        schedule.append(
            AmortizationRow(
                month=month,
                payment=total_payment,
                principal=principal_paid,
                interest=interest,
                balance=balance,
            )
        )

    return schedule


def loan_summary(loan: LoanInput) -> LoanResult:
    schedule = amortization_schedule(loan)
    total_paid = sum(row.payment for row in schedule)
    total_interest = sum(row.interest for row in schedule)
    years = len(schedule) / 12
    monthly_payment = compute_monthly_payment(loan)

    return LoanResult(
        monthly_payment=monthly_payment,
        total_interest=total_interest,
        total_paid=total_paid,
        years=years,
    )
