from qfinancetools.core.comparison import compare_scenarios
from qfinancetools.models.comparison import ComparisonCase, ComparisonRequest


def test_compare_loan() -> None:
    result = compare_scenarios(
        ComparisonRequest(
            calculator="loan",
            base=ComparisonCase(label="Base", inputs={"amount": 300000, "rate": 5.4, "years": 25, "extra": 0}),
            alt=ComparisonCase(label="Alt", inputs={"amount": 300000, "rate": 4.8, "years": 25, "extra": 0}),
        )
    )
    assert result.calculator == "loan"
    assert len(result.deltas) == 4


def test_compare_invest() -> None:
    result = compare_scenarios(
        ComparisonRequest(
            calculator="invest",
            base=ComparisonCase(label="Base", inputs={"initial": 10000, "monthly": 500, "rate": 7, "years": 20}),
            alt=ComparisonCase(label="Alt", inputs={"initial": 10000, "monthly": 600, "rate": 7, "years": 20}),
        )
    )
    assert result.calculator == "invest"
    assert any(item.metric == "final_value" for item in result.deltas)
