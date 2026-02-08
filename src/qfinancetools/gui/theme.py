from __future__ import annotations

from pathlib import Path

from PySide6 import QtGui


ASSET_DIR = Path(__file__).resolve().parent / "assets" / "fonts"


def load_fonts() -> None:
    # Optional font loading. If files are missing, we fall back to system fonts.
    font_files = [
        ASSET_DIR / "SpaceGrotesk-Regular.ttf",
        ASSET_DIR / "SpaceGrotesk-SemiBold.ttf",
    ]
    for path in font_files:
        if path.exists():
            QtGui.QFontDatabase.addApplicationFont(str(path))


def app_stylesheet() -> str:
    return """
    QWidget {
        color: #111827;
        font-family: "Space Grotesk", "Fira Sans", "Helvetica Neue", sans-serif;
        font-size: 13px;
    }
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #f8fafc, stop:1 #eef2f7);
    }
    QLabel#HeaderTitle {
        font-size: 24px;
        font-weight: 600;
    }
    QLabel#HeaderSubtitle {
        color: #6b7280;
    }
    QListWidget {
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 6px;
    }
    QListWidget::item {
        padding: 10px 12px;
        border-radius: 8px;
    }
    QListWidget::item:selected {
        background: #e2e8f0;
        color: #0f172a;
        font-weight: 600;
    }
    QLineEdit, QDoubleSpinBox, QSpinBox {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 6px 8px;
        selection-background-color: #0ea5e9;
    }
    QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus {
        border: 1px solid #0ea5e9;
        background: #f0f9ff;
    }
    QPushButton {
        background: #0ea5e9;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 14px;
    }
    QPushButton:hover {
        background: #0284c7;
    }
    QPushButton:pressed {
        background: #0369a1;
    }
    QTabWidget::pane {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        background: #ffffff;
    }
    QTabBar::tab {
        padding: 9px 14px;
        margin: 4px;
        border-radius: 8px;
        background: #f1f5f9;
        font-weight: 600;
    }
    QTabBar::tab:selected {
        background: #0ea5e9;
        color: white;
    }
    QFrame#ResultCard {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
    }
    QLabel#ResultCardTitle {
        color: #6b7280;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    QLabel#ResultCardValue {
        font-size: 18px;
        font-weight: 600;
    }
    QLabel#ErrorBanner {
        background: #fef2f2;
        color: #b91c1c;
        border: 1px solid #fecaca;
        border-radius: 8px;
        padding: 8px;
    }
    QTableWidget {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
    }
    QHeaderView::section {
        background: #f8fafc;
        border: none;
        padding: 6px;
        font-weight: 600;
    }
    """
