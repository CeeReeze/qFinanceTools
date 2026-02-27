from __future__ import annotations

from qfinancetools.core.bonds import bond_price
from qfinancetools.core.guardrails import bonds_warnings, invest_warnings, loan_warnings
from qfinancetools.core.investments import investment_growth
from qfinancetools.core.loans import loan_summary
from qfinancetools.core.stocks import stock_projection
from qfinancetools.models.bonds import BondPriceInput
from qfinancetools.models.investments import InvestmentInput
from qfinancetools.models.loans import LoanInput
from qfinancetools.models.stocks import StockProjectionInput
from qfinancetools.models.timeline import TimelinePoint, TimelineRequest, TimelineResult, TimelineSeries


def _flow_points(amounts: list[float]) -> list[TimelinePoint]:
    running = 0.0
    points: list[TimelinePoint] = []
    for idx, amount in enumerate(amounts, start=1):
        running += amount
        points.append(TimelinePoint(month=idx, amount=amount, running_total=running))
    return points


def build_unified_timeline(
    request: TimelineRequest,
    loan_input: LoanInput | None = None,
    invest_input: InvestmentInput | None = None,
    bond_input: BondPriceInput | None = None,
    stock_input: StockProjectionInput | None = None,
) -> TimelineResult:
    loan_flows = [0.0] * request.months
    invest_flows = [0.0] * request.months
    bond_flows = [0.0] * request.months
    stock_flows = [0.0] * request.months
    warnings = []

    if request.include_loan and loan_input is not None:
        monthly_payment = loan_summary(loan_input).monthly_payment + loan_input.extra_payment
        payoff_month = min(loan_input.years * 12, request.months)
        for month_idx in range(payoff_month):
            loan_flows[month_idx] = -monthly_payment
        warnings.extend(loan_warnings(loan_input.principal, loan_input.annual_rate, loan_input.years, loan_input.extra_payment))

    if request.include_invest and invest_input is not None:
        months = min(invest_input.years * 12, request.months)
        for month_idx in range(months):
            invest_flows[month_idx] = -invest_input.monthly
        invested_result = investment_growth(invest_input)
        invest_flows[months - 1] += invested_result.final_value
        warnings.extend(invest_warnings(invest_input.initial, invest_input.monthly, invest_input.annual_rate, invest_input.years))

    if request.include_bonds and bond_input is not None:
        coupon = bond_input.face_value * bond_input.coupon_rate / 100 / bond_input.payments_per_year
        step = max(1, round(12 / bond_input.payments_per_year))
        maturity_month = min(bond_input.years * 12, request.months)
        for month in range(step, maturity_month + 1, step):
            bond_flows[month - 1] += coupon
        if maturity_month > 0:
            bond_flows[maturity_month - 1] += bond_input.face_value
        _ = bond_price(bond_input)
        warnings.extend(bonds_warnings(bond_input.yield_rate, bond_input.coupon_rate, bond_input.years))

    if request.include_stocks and stock_input is not None:
        months = min(stock_input.years * 12, request.months)
        for month_idx in range(months):
            stock_flows[month_idx] = -stock_input.monthly
        stock_result = stock_projection(stock_input)
        stock_flows[months - 1] += stock_result.final_value
        warnings.extend(stock_result.warnings)

    net_flows = [loan_flows[i] + invest_flows[i] + bond_flows[i] + stock_flows[i] for i in range(request.months)]
    series = [
        TimelineSeries(name="Loan", points=_flow_points(loan_flows)),
        TimelineSeries(name="Investment", points=_flow_points(invest_flows)),
        TimelineSeries(name="Bonds", points=_flow_points(bond_flows)),
        TimelineSeries(name="Stocks/ETF", points=_flow_points(stock_flows)),
    ]
    return TimelineResult(months=request.months, series=series, net=_flow_points(net_flows), warnings=warnings)
