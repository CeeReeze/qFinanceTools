from __future__ import annotations

import sys

from PySide6 import QtCore, QtWidgets

from qfinancetools.gui import theme
from qfinancetools.gui.pages.afford_page import AffordPage
from qfinancetools.gui.pages.bonds_page import BondsPage
from qfinancetools.gui.pages.corporate_page import CorporatePage
from qfinancetools.gui.pages.invest_page import InvestPage
from qfinancetools.gui.pages.loan_page import LoanPage
from qfinancetools.gui.pages.risk_page import RiskPage


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("qFinance Tools")
        self.resize(1200, 800)

        root = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(root)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        header = QtWidgets.QWidget()
        header_layout = QtWidgets.QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(2)
        title = QtWidgets.QLabel("qFinance Tools")
        title.setObjectName("HeaderTitle")
        subtitle = QtWidgets.QLabel("Model-driven finance calculators with visual output")
        subtitle.setObjectName("HeaderSubtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        body = QtWidgets.QWidget()
        body_layout = QtWidgets.QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(16)

        self.nav = QtWidgets.QListWidget()
        self.nav.setFixedWidth(200)
        self.nav.addItems(["Loan", "Invest", "Afford", "Corporate", "Bonds", "Risk"])
        self.nav.currentRowChanged.connect(self._on_nav_changed)

        self.stack = QtWidgets.QStackedWidget()
        self.pages = [
            LoanPage(),
            InvestPage(),
            AffordPage(),
            CorporatePage(),
            BondsPage(),
            RiskPage(),
        ]
        for page in self.pages:
            self.stack.addWidget(page)

        body_layout.addWidget(self.nav)
        body_layout.addWidget(self.stack, 1)

        layout.addWidget(header)
        layout.addWidget(body, 1)
        self.setCentralWidget(root)

        self.nav.setCurrentRow(0)

    def _on_nav_changed(self, index: int) -> None:
        if 0 <= index < self.stack.count():
            self.stack.setCurrentIndex(index)


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    theme.load_fonts()
    app.setStyleSheet(theme.app_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
