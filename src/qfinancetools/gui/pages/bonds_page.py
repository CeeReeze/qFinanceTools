from __future__ import annotations

from PySide6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from qfinancetools.core.bonds import bond_price, bond_ytm, bond_duration, bond_convexity, bond_ladder
from qfinancetools.models.bonds import (
    BondPriceInput,
    BondYtmInput,
    BondDurationInput,
    BondConvexityInput,
    BondLadderInput,
)
from qfinancetools.gui.widgets import (
    labeled_field,
    make_error_banner,
    make_form,
    make_primary_button,
    show_error,
    ResultCard,
    parse_list_floats,
    parse_list_ints,
    annotate_bars,
    apply_chart_theme,
    format_currency_axis,
)


class BondsPage(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self._build_price_tab(), "Price")
        tabs.addTab(self._build_ytm_tab(), "YTM")
        tabs.addTab(self._build_duration_tab(), "Duration")
        tabs.addTab(self._build_convexity_tab(), "Convexity")
        tabs.addTab(self._build_ladder_tab(), "Ladder")
        layout.addWidget(tabs)

    def _build_price_tab(self) -> QtWidgets.QWidget:
        return _bond_simple_tab(
            title="Bond price",
            calculator=self._price_calc,
        )

    def _build_ytm_tab(self) -> QtWidgets.QWidget:
        return _bond_simple_tab(
            title="Yield to maturity",
            calculator=self._ytm_calc,
        )

    def _build_duration_tab(self) -> QtWidgets.QWidget:
        return _bond_simple_tab(
            title="Duration",
            calculator=self._duration_calc,
            extra_card=ResultCard("Modified", "0"),
        )

    def _build_convexity_tab(self) -> QtWidgets.QWidget:
        return _bond_simple_tab(
            title="Convexity",
            calculator=self._convexity_calc,
        )

    def _build_ladder_tab(self) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setSpacing(16)

        maturities = QtWidgets.QLineEdit("1, 3, 5, 7, 10")
        amounts = QtWidgets.QLineEdit("5000, 5000, 5000, 5000, 5000")

        form = make_form(
            [
                labeled_field("Maturities (years)", maturities),
                labeled_field("Amounts", amounts),
            ]
        )

        left = QtWidgets.QVBoxLayout()
        left.addWidget(form)
        left.addStretch(1)
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left)

        right = QtWidgets.QVBoxLayout()
        error = make_error_banner()
        right.addWidget(error)
        card_total = ResultCard("Total invested", "$0")
        card_weighted = ResultCard("Weighted maturity", "0")
        cards = QtWidgets.QHBoxLayout()
        cards.addWidget(card_total)
        cards.addWidget(card_weighted)
        right.addLayout(cards)
        figure = Figure(figsize=(5, 3))
        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(240)
        right.addWidget(canvas, 2)
        right.addStretch(1)

        def calculate() -> None:
            try:
                mats = parse_list_ints(maturities.text())
                amts = parse_list_floats(amounts.text())
                data = BondLadderInput(maturities=mats, amounts=amts)
                result = bond_ladder(data)
                show_error(error, None)
            except Exception as exc:
                show_error(error, str(exc))
                return
            card_total.set_value(f"${result.total_invested:,.2f}")
            card_weighted.set_value(f"{result.weighted_maturity:.2f} years")
            figure.clear()
            ax = figure.add_subplot(111)
            labels = [str(m) for m, _ in result.schedule]
            values = [a for _, a in result.schedule]
            ax.bar(labels, values, color="#0ea5e9")
            ax.plot(labels, values, color="#0f172a", marker="o", linewidth=1)
            ax.set_xlabel("Maturity (years)")
            ax.set_ylabel("Amount")
            apply_chart_theme(ax)
            format_currency_axis(ax, "y")
            annotate_bars(ax, fmt="${:,.0f}")
            figure.tight_layout()
            canvas.draw()

        left.addWidget(make_primary_button("Calculate", calculate))
        calculate()

        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([320, 800])
        layout.addWidget(splitter)
        return widget

    def _price_calc(self, inputs):
        data = BondPriceInput(
            face_value=inputs["face"].value(),
            coupon_rate=inputs["coupon"].value(),
            yield_rate=inputs["ytm"].value(),
            years=inputs["years"].value(),
            payments_per_year=inputs["freq"].value(),
        )
        result = bond_price(data)
        return {
            "Primary": f"${result.price:,.2f}",
        }

    def _ytm_calc(self, inputs):
        data = BondYtmInput(
            face_value=inputs["face"].value(),
            coupon_rate=inputs["coupon"].value(),
            price=inputs["price"].value(),
            years=inputs["years"].value(),
            payments_per_year=inputs["freq"].value(),
        )
        result = bond_ytm(data)
        return {
            "Primary": f"{result.yield_rate:.3f}%",
        }

    def _duration_calc(self, inputs):
        data = BondDurationInput(
            face_value=inputs["face"].value(),
            coupon_rate=inputs["coupon"].value(),
            yield_rate=inputs["ytm"].value(),
            years=inputs["years"].value(),
            payments_per_year=inputs["freq"].value(),
        )
        result = bond_duration(data)
        return {
            "Primary": f"{result.macaulay_duration:.4f}",
            "Modified": f"{result.modified_duration:.4f}",
        }

    def _convexity_calc(self, inputs):
        data = BondConvexityInput(
            face_value=inputs["face"].value(),
            coupon_rate=inputs["coupon"].value(),
            yield_rate=inputs["ytm"].value(),
            years=inputs["years"].value(),
            payments_per_year=inputs["freq"].value(),
        )
        result = bond_convexity(data)
        return {
            "Primary": f"{result.convexity:.4f}",
        }


def _bond_simple_tab(
    title: str,
    calculator,
    extra_card: ResultCard | None = None,
) -> QtWidgets.QWidget:
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)
    layout.setSpacing(16)

    face = QtWidgets.QDoubleSpinBox()
    face.setRange(0, 1_000_000)
    face.setValue(1000)

    coupon = QtWidgets.QDoubleSpinBox()
    coupon.setRange(0, 100)
    coupon.setValue(5)
    coupon.setSuffix("%")
    coupon.setDecimals(3)

    ytm = QtWidgets.QDoubleSpinBox()
    ytm.setRange(0, 100)
    ytm.setValue(4.5)
    ytm.setSuffix("%")
    ytm.setDecimals(3)

    years = QtWidgets.QSpinBox()
    years.setRange(1, 100)
    years.setValue(10)

    freq = QtWidgets.QSpinBox()
    freq.setRange(1, 12)
    freq.setValue(2)

    price = QtWidgets.QDoubleSpinBox()
    price.setRange(0, 1_000_000)
    price.setValue(980)

    inputs = {
        "face": face,
        "coupon": coupon,
        "ytm": ytm,
        "years": years,
        "freq": freq,
        "price": price,
    }

    if title == "Yield to maturity":
        fields = [
            labeled_field("Face value", face),
            labeled_field("Coupon rate", coupon),
            labeled_field("Bond price", price),
            labeled_field("Years", years),
            labeled_field("Payments/year", freq),
        ]
    else:
        fields = [
            labeled_field("Face value", face),
            labeled_field("Coupon rate", coupon),
            labeled_field("Yield to maturity", ytm),
            labeled_field("Years", years),
            labeled_field("Payments/year", freq),
        ]

    form = make_form(fields)

    left = QtWidgets.QVBoxLayout()
    left.addWidget(form)
    left.addStretch(1)
    left_widget = QtWidgets.QWidget()
    left_widget.setLayout(left)

    right = QtWidgets.QVBoxLayout()
    error = make_error_banner()
    right.addWidget(error)
    primary = ResultCard(title, "0")
    right.addWidget(primary)
    if extra_card:
        right.addWidget(extra_card)
    right.addStretch(1)

    def calculate() -> None:
        try:
            result = calculator(inputs)
            show_error(error, None)
        except Exception as exc:
            show_error(error, str(exc))
            return
        primary.set_value(result.get("Primary", "0"))
        if extra_card:
            extra_card.set_value(result.get("Modified", "0"))

    left.addWidget(make_primary_button("Calculate", calculate))
    calculate()

    right_widget = QtWidgets.QWidget()
    right_widget.setLayout(right)

    splitter = QtWidgets.QSplitter()
    splitter.addWidget(left_widget)
    splitter.addWidget(right_widget)
    splitter.setStretchFactor(0, 0)
    splitter.setStretchFactor(1, 1)
    splitter.setSizes([320, 800])
    layout.addWidget(splitter)
    return widget
